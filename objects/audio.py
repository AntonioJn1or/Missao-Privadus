"""Carregamento compartilhado de efeitos e música do jogo."""

from pathlib import Path

import pygame


class Audio:
    _SOUND_DIR = Path(__file__).resolve().parents[1] / "assets/sounds"
    _sounds = {}
    _music_path = None

    @classmethod
    def _ensure_mixer(cls):
        if pygame.mixer.get_init() is None:
            pygame.mixer.init()

    @classmethod
    def play_effect(cls, filename):
        try:
            cls._ensure_mixer()
            sound = cls._sounds.get(filename)
            if sound is None:
                sound = pygame.mixer.Sound(str(cls._SOUND_DIR / filename))
                cls._sounds[filename] = sound
            sound.play()
        except (pygame.error, OSError):
            # Áudio indisponível não deve impedir a execução do jogo.
            return False
        return True

    @classmethod
    def play_music(cls, filename):
        path = cls._SOUND_DIR / filename
        try:
            cls._ensure_mixer()
            if cls._music_path == path and pygame.mixer.music.get_busy():
                return True
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.set_volume(0.55)
            pygame.mixer.music.play(-1)
            cls._music_path = path
        except (pygame.error, OSError):
            cls._music_path = None
            return False
        return True

    @classmethod
    def stop_music(cls):
        try:
            if pygame.mixer.get_init() is not None:
                pygame.mixer.music.stop()
        except pygame.error:
            pass
        cls._music_path = None
