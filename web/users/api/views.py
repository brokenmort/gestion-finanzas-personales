# -*- coding: latin-1 -*-
import random
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from users.api.serializers import (
    UserRegisterSerializer, UserUpdateSerializer,
    PasswordResetRequestSerializer, PasswordResetVerifySerializer,
    PasswordResetConfirmSerializer,
    SignupRequestSerializer, SignupVerifySerializer,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from users.models import User, PasswordResetToken
from users.models import PasswordResetCode, PendingSignup
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken

# ✅ Importante: incluir JSONParser para aceptar application/json
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from .utils import approve_signup_and_send_code
from django.utils import timezone


# -----------------------------------------------------------
# VISTA DE REGISTRO DE USUARIO
# -----------------------------------------------------------
class RegisterView(APIView):
    """
    Vista para registrar nuevos usuarios.
    Permite subir imagen de perfil usando multipart/form-data.
    También acepta JSON cuando no se envía archivo.
    """
    permission_classes = [AllowAny]
    # ✅ FIX: ahora acepta JSON también
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary='Registro de usuario',
        tags=['Auth'],
        operation_description='Crea un usuario nuevo. Envía multipart/form-data si incluye profile_image, o JSON si no envía archivo.',
        consumes=['multipart/form-data', 'application/json'],
        manual_parameters=[
            openapi.Parameter('email', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, description='Correo'),
            openapi.Parameter('password', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, description='Contraseña'),
            openapi.Parameter('birthday', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, description='YYYY-MM-DD'),
            openapi.Parameter('first_name', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('last_name', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('phone', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('country', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('profile_image', openapi.IN_FORM, type=openapi.TYPE_FILE, required=False)
        ],
        responses={
            201: openapi.Response(
                description='Usuario creado',
                examples={'application/json': {'id': 1, 'email': 'user@mail.com'}}
            )
        }
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# -----------------------------------------------------------
# SOLICITUD DE REGISTRO (envía código al admin)
# -----------------------------------------------------------
class SignupRequestView(APIView):
    permission_classes = [AllowAny]
    # (acepta JSON por default gracias a settings.py)

    def post(self, request):
        s = SignupRequestSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        data = s.validated_data
        email = data["email"].lower()

        if User.objects.filter(email=email).exists():
            return Response({"error": "Ya existe un usuario con ese correo."}, status=400)

        extra = {
            "password": data["password"],
            "birthday": str(data["birthday"]),
            "phone": data["phone"],
            "country": data["country"],
        }
        pending, created = PendingSignup.objects.get_or_create(
            email=email,
            defaults={
                "first_name": data.get("first_name", ""),
                "last_name": data.get("last_name", ""),
                "extra_info": extra,
            },
        )
        if not created:
            pending.first_name = data.get("first_name", "")
            pending.last_name = data.get("last_name", "")
            pending.extra_info = extra
            pending.save()

        code = str(random.randint(10000000, 99999999))
        PasswordResetCode.objects.create(
            user_email=email,
            code=code,
            purpose="signup",
            expires_at=timezone.now() + timezone.timedelta(minutes=30),
        )

        admin_email = getattr(settings, "ADMIN_SIGNUP_EMAIL", "giraldovnelson@gmail.com")
        body = (
            "Nueva solicitud de registro\n\n"
            f"Email: {email}\n"
            f"Nombre: {pending.first_name} {pending.last_name}\n"
            f"Telefono: {extra['phone']}\n"
            f"Pais: {extra['country']}\n"
            f"Cumpleanos: {extra['birthday']}\n\n"
            f"Codigo de verificacion (compartir al solicitante): {code}\n"
        )
        send_mail(
            subject="Nueva solicitud de registro",
            message=body,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@localhost"),
            recipient_list=[admin_email],
            fail_silently=True,
        )

        return Response({"message": "Solicitud enviada. Espera el codigo del administrador."}, status=200)


# -----------------------------------------------------------
# VERIFICAR CÓDIGO DE REGISTRO Y CREAR CUENTA
# -----------------------------------------------------------
class SignupVerifyView(APIView):
    permission_classes = [AllowAny]
    # (acepta JSON por default gracias a settings.py)

    def post(self, request):
        s = SignupVerifySerializer(data=request.data)
        s.is_valid(raise_exception=True)
        email = s.validated_data["email"].lower()
        token = s.validated_data["token"]

        try:
            pending = PendingSignup.objects.get(email=email)
        except PendingSignup.DoesNotExist:
            return Response({"error": "No hay una solicitud pendiente para este correo."}, status=404)

        prc = PasswordResetCode.objects.filter(
            user_email=email, code=token, purpose="signup"
        ).order_by("-created_at").first()
        if not prc or not prc.is_valid():
            return Response({"error": "Codigo invalido o expirado."}, status=400)

        extra = pending.extra_info or {}
        user = User(
            email=email,
            first_name=pending.first_name or "",
            last_name=pending.last_name or "",
            birthday=extra.get("birthday", "2000-01-01"),
            phone=extra.get("phone", "0000000000"),
            country=extra.get("country", "Unknown"),
        )
        pwd = extra.get("password") or "changeme12345"
        user.set_password(pwd)
        user.save()

        prc.delete()
        pending.delete()

        return Response({"message": "Cuenta creada correctamente. Ya puedes iniciar sesion."}, status=200)


# -----------------------------------------------------------
# VISTA DE PERFIL DE USUARIO
# -----------------------------------------------------------
class userView(APIView):
    """
    Vista para obtener y actualizar información del usuario autenticado.
    """
    permission_classes = [IsAuthenticated]
    # ✅ FIX: ahora acepta JSON también (además de multipart para imagen)
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary='Perfil del usuario (detalle)', tags=['Usuarios'],
        responses={200: openapi.Response('OK', examples={'application/json': {
            'id': 1,
            'email': 'user@mail.com',
            'birthday': '2000-01-01',
            'first_name': 'Nelson',
            'last_name': 'Giraldo',
            'phone': '3000000000',
            'country': 'CO',
            'profile_image': None
        }})}
    )
    def get(self, request):
        serializer = UserRegisterSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary='Actualizar perfil de usuario', tags=['Usuarios'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, example='Nelson'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, example='Giraldo'),
                'birthday': openapi.Schema(type=openapi.TYPE_STRING, example='2000-01-01'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, example='3000000000'),
                'country': openapi.Schema(type=openapi.TYPE_STRING, example='CO'),
                'profile_image': openapi.Schema(type=openapi.TYPE_STRING, format='binary')
            }
        )
    )
    def put(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserUpdateSerializer(user, context={'request': request}).data)


# -----------------------------------------------------------
# SOLICITUD DE RESET DE CONTRASEÑA
# -----------------------------------------------------------
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Solicitar codigo de reseteo', tags=['Auth'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={'email': openapi.Schema(type=openapi.TYPE_STRING, example='user@mail.com')}
        ),
        responses={200: openapi.Response('OK', examples={'application/json': {'detail': 'Codigo enviado'}})}
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "No existe un usuario con ese correo."}, status=404)

        token = str(random.randint(10000000, 99999999))
        PasswordResetToken.objects.create(user=user, token=token)

        send_mail(
            subject="Recuperacion de contrasena - Gestion finanzas personales",
            message=f"Tu codigo de verificacion es: {token} (valido por 15 minutos). Si no solicitaste este cambio, ignora este correo.",
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@localhost"),
            recipient_list=[email],
            fail_silently=True
        )
        return Response({"message": "Se ha enviado un codigo al correo."}, status=200)


class PasswordResetVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        token = serializer.validated_data["token"]

        try:
            user = User.objects.get(email=email)
            reset_token = PasswordResetToken.objects.filter(user=user, token=token).last()
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=404)

        if reset_token and reset_token.is_valid():
            return Response({"valid": True}, status=200)

        return Response({"valid": False}, status=400)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Confirmar reseteo de contrasena', tags=['Auth'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'token', 'new_password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, example='user@mail.com'),
                'token': openapi.Schema(type=openapi.TYPE_STRING, example='12345678'),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, example='newPass123')
            }
        ),
        responses={200: openapi.Response('OK', examples={'application/json': {'message': 'Contrasena actualizada y sesiones cerradas.'}})}
    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        try:
            user = User.objects.get(email=email)
            reset_token = PasswordResetToken.objects.filter(user=user, token=token).last()
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=404)

        if reset_token and reset_token.is_valid():
            user.set_password(new_password)
            user.save()

            for outstanding_token in OutstandingToken.objects.filter(user=user):
                BlacklistedToken.objects.get_or_create(token=outstanding_token)

            reset_token.delete()
            return Response({"message": "Contraseña actualizada y sesiones cerradas."}, status=200)

        return Response({"error": "Token inválido o expirado."}, status=400)


# -----------------------------------------------------------
# LOGIN Y REFRESH DE TOKENS JWT
# -----------------------------------------------------------
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Login (JWT pair)',
        tags=['Auth'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, example='user@mail.com'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, example='******'),
            }
        ),
        responses={
            200: openapi.Response(
                description='Tokens',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
                examples={'application/json': {
                    'access': 'eyJhbGciOi...access...',
                    'refresh': 'eyJhbGciOi...refresh...'
                }}
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Refrescar access token',
        tags=['Auth'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={'refresh': openapi.Schema(type=openapi.TYPE_STRING)}
        ),
        responses={
            200: openapi.Response(
                description='Nuevo access',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={'access': openapi.Schema(type=openapi.TYPE_STRING)}
                ),
                examples={'application/json': {'access': 'eyJhbGciOi...access...'}}
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# -----------------------------------------------------------
# LOGOUT DE USUARIO
# -----------------------------------------------------------
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Logout (revocar tokens)',
        tags=['Auth'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'refresh': openapi.Schema(type=openapi.TYPE_STRING)},
            description='Opcional: si no se envía refresh, se revocan todos los tokens del usuario.'
        )
    )
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh", None)
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(
                    {"detail": "Logout exitoso (refresh token revocado)."},
                    status=status.HTTP_205_RESET_CONTENT
                )

            tokens = OutstandingToken.objects.filter(user=request.user)
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)

            return Response(
                {"detail": "Logout exitoso (todos los tokens revocados)."},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------------------------------
# VISTA DE INFORMACIÓN BÁSICA DEL USUARIO
# -----------------------------------------------------------
class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Info basica del usuario', tags=['Usuarios'],
        responses={200: openapi.Response('OK', examples={'application/json': {
            'username': None,
            'email': 'user@mail.com',
            'id': 1,
            'profile_image': None
        }})}
    )
    def get(self, request):
        user = request.user
        img_url = None
        try:
            if user.profile_image:
                img_url = user.profile_image.url
        except Exception:
            img_url = None
        if img_url and not str(img_url).startswith(("http://", "https://")):
            img_url = request.build_absolute_uri(img_url)

        return Response({
            "username": user.username,
            "email": user.email,
            "id": user.id,
            "profile_image": img_url
        })


def _is_superuser(user):
    return user.is_authenticated and user.is_superuser


@login_required
@user_passes_test(_is_superuser)
@transaction.atomic
def approve_signup_view(request, token: str):
    if request.method != "GET":
        return HttpResponseBadRequest("Método no permitido.")
    try:
        approve_signup_and_send_code(token)
    except Exception as e:
        return HttpResponseBadRequest(f"Error: {e}")
    return HttpResponse("Solicitud aprobada y código enviado al solicitante.")
