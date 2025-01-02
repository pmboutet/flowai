from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..services.google_drive import GoogleDriveService
from ..models import UserGoogleAuth, Session, Sequence

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_session_folder(request):
    """Crée une structure de dossiers pour une nouvelle session"""
    try:
        session_id = request.data.get('session_id')
        session = Session.objects.get(id=session_id, user=request.user)

        drive_service = GoogleDriveService(request.user)

        # Crée le dossier principal de la session
        session_folder = drive_service.create_folder(
            f'Session - {session.title} - {session.client.name}'
        )

        # Crée un dossier pour chaque séquence
        for sequence in session.sequences.all():
            sequence_folder = drive_service.create_folder(
                f'Sequence {sequence.order} - {sequence.title}',
                session_folder['id']
            )

            # Crée les sous-dossiers inputs/outputs
            input_folder = drive_service.create_folder('Inputs', sequence_folder['id'])
            output_folder = drive_service.create_folder('Outputs', sequence_folder['id'])

            # Met à jour les URLs dans la séquence
            sequence.input_drive_url = input_folder['webViewLink']
            sequence.output_drive_url = output_folder['webViewLink']
            sequence.save()

            # Partage avec le client si nécessaire
            if session.client.email:
                drive_service.share_file(sequence_folder['id'], session.client.email)

        return Response({
            'message': 'Structure de dossiers créée avec succès',
            'session_folder_url': session_folder['webViewLink']
        })

    except Session.DoesNotExist:
        return Response(
            {'error': 'Session non trouvée'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_drive_access(request):
    """Vérifie si l'utilisateur a accès à Google Drive"""
    try:
        google_auth = UserGoogleAuth.objects.get(user=request.user)
        return Response({
            'drive_enabled': google_auth.drive_enabled,
            'token_valid': google_auth.is_token_valid()
        })
    except UserGoogleAuth.DoesNotExist:
        return Response({
            'drive_enabled': False,
            'token_valid': False
        })

@login_required
def google_oauth_callback(request):
    """Callback pour l'authentification Google"""
    try:
        # Met à jour ou crée les informations d'authentification
        google_auth, created = UserGoogleAuth.objects.update_or_create(
            user=request.user,
            defaults={
                'google_id': request.session.get('google_id'),
                'access_token': request.session.get('access_token'),
                'refresh_token': request.session.get('refresh_token'),
                'token_expiry': timezone.now() + timezone.timedelta(hours=1),
                'drive_enabled': True
            }
        )
        return redirect('admin:index')
    except Exception as e:
        return redirect('admin:index')