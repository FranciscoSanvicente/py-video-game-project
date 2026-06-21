"""Interfaz grafica con Pygame: menu, juego, registro de ganador y records.

Toda la parte visual y de interaccion vive aqui. La logica del juego se delega
en :class:`~memory_game.game.Game`, y la persistencia en
:class:`~memory_game.scores.ScoreBoard`.
"""

from __future__ import annotations

import datetime

import pygame

from . import config as cfg
from .assets import load_pair_images
from .game import Game
from .models import TurnResult
from .scores import Score, ScoreBoard

# Estados (pantallas) de la aplicacion.
MENU, PLAYING, WON, SCORES = "menu", "playing", "won", "scores"


class App:
    """Aplicacion principal: gestiona pantallas, eventos y dibujo."""

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(cfg.TITLE)
        self.screen = pygame.display.set_mode((cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Fuentes reutilizables.
        self.font_xl = pygame.font.SysFont("arial", 56, bold=True)
        self.font_lg = pygame.font.SysFont("arial", 34, bold=True)
        self.font_md = pygame.font.SysFont("arial", 26)
        self.font_sm = pygame.font.SysFont("arial", 20)

        self.scoreboard = ScoreBoard()
        self.state = MENU
        self.difficulty = cfg.DEFAULT_DIFFICULTY

        # Estado de partida (se crean al iniciar una nueva).
        self.game: Game | None = None
        self.images: dict[int, pygame.Surface] = {}
        self.card_size = 0
        self.origin = (0, 0)
        self.gap = 12
        self._mismatch_at: int | None = None   # Momento del desajuste (ticks).
        self.name_input = ""                    # Texto del ganador en pantalla WON.

    # ======================================================================
    # Bucle principal
    # ======================================================================
    def run(self) -> None:
        """Bucle de juego: eventos -> actualizacion -> dibujo, a ``FPS``."""
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(cfg.FPS)
        pygame.quit()

    # ======================================================================
    # Nueva partida
    # ======================================================================
    def _start_game(self) -> None:
        rows, cols = cfg.DIFFICULTIES[self.difficulty]
        self.game = Game(rows, cols)
        self._mismatch_at = None
        self._compute_layout(rows, cols)
        self.images = load_pair_images(self.game.board.num_pairs, self.card_size)
        self.state = PLAYING

    def _compute_layout(self, rows: int, cols: int) -> None:
        """Calcula tamano de carta y origen para centrar el tablero."""
        hud_h = 110
        margin = 30
        avail_w = cfg.WINDOW_WIDTH - 2 * margin
        avail_h = cfg.WINDOW_HEIGHT - hud_h - margin
        size_w = (avail_w - (cols - 1) * self.gap) / cols
        size_h = (avail_h - (rows - 1) * self.gap) / rows
        self.card_size = int(min(size_w, size_h))
        grid_w = cols * self.card_size + (cols - 1) * self.gap
        grid_h = rows * self.card_size + (rows - 1) * self.gap
        origin_x = (cfg.WINDOW_WIDTH - grid_w) // 2
        origin_y = hud_h + (avail_h - grid_h) // 2
        self.origin = (origin_x, origin_y)

    def _card_rect(self, row: int, col: int) -> pygame.Rect:
        ox, oy = self.origin
        x = ox + col * (self.card_size + self.gap)
        y = oy + row * (self.card_size + self.gap)
        return pygame.Rect(x, y, self.card_size, self.card_size)

    # ======================================================================
    # Eventos
    # ======================================================================
    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.state == MENU:
                self._events_menu(event)
            elif self.state == PLAYING:
                self._events_playing(event)
            elif self.state == WON:
                self._events_won(event)
            elif self.state == SCORES:
                self._events_scores(event)

    def _events_menu(self, event: pygame.event.Event) -> None:
        names = list(cfg.DIFFICULTIES)
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_LEFT):
                i = names.index(self.difficulty)
                self.difficulty = names[(i - 1) % len(names)]
            elif event.key in (pygame.K_DOWN, pygame.K_RIGHT):
                i = names.index(self.difficulty)
                self.difficulty = names[(i + 1) % len(names)]
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self._start_game()
            elif event.key == pygame.K_p:
                self.state = SCORES
            elif event.key == pygame.K_ESCAPE:
                self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self._menu_difficulty_rects()):
                if rect.collidepoint(event.pos):
                    self.difficulty = names[i]
            if self._menu_play_rect().collidepoint(event.pos):
                self._start_game()
            elif self._menu_scores_rect().collidepoint(event.pos):
                self.state = SCORES

    def _events_playing(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state = MENU
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.game is None or self.game.waiting_for_mismatch:
                return
            cell = self._cell_at_pixel(event.pos)
            if cell is None:
                return
            row, col = cell
            result = self.game.select(row, col)
            if result == TurnResult.MISMATCH:
                self._mismatch_at = pygame.time.get_ticks()
            elif result == TurnResult.MATCH and self.game.won:
                self._enter_won_state()

    def _events_won(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self._save_winner()
        elif event.key == pygame.K_BACKSPACE:
            self.name_input = self.name_input[:-1]
        elif len(self.name_input) < 16 and event.unicode.isprintable():
            self.name_input += event.unicode

    def _events_scores(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.state = MENU

    def _cell_at_pixel(self, pos: tuple[int, int]) -> tuple[int, int] | None:
        """Convierte coordenadas de pixel en (fila, columna), o None."""
        assert self.game is not None
        for row in range(self.game.board.rows):
            for col in range(self.game.board.cols):
                if self._card_rect(row, col).collidepoint(pos):
                    return (row, col)
        return None

    # ======================================================================
    # Transiciones de fin de partida
    # ======================================================================
    def _enter_won_state(self) -> None:
        self.name_input = ""
        self.state = WON

    def _save_winner(self) -> None:
        assert self.game is not None
        name = self.name_input.strip() or "Anonimo"
        score = Score(
            name=name,
            moves=self.game.moves,
            seconds=round(self.game.elapsed_seconds(), 1),
            difficulty=self.difficulty,
            date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        )
        self.scoreboard.add(score)
        self.state = SCORES

    # ======================================================================
    # Actualizacion
    # ======================================================================
    def _update(self) -> None:
        if self.state == PLAYING and self._mismatch_at is not None:
            assert self.game is not None
            if pygame.time.get_ticks() - self._mismatch_at >= cfg.MISMATCH_DELAY_MS:
                self.game.resolve_mismatch()
                self._mismatch_at = None

    # ======================================================================
    # Dibujo
    # ======================================================================
    def _draw(self) -> None:
        self.screen.fill(cfg.COLOR_BG)
        if self.state == MENU:
            self._draw_menu()
        elif self.state == PLAYING:
            self._draw_playing()
        elif self.state == WON:
            self._draw_playing()      # Tablero resuelto de fondo.
            self._draw_won_overlay()
        elif self.state == SCORES:
            self._draw_scores()
        pygame.display.flip()

    def _text(self, text: str, font: pygame.font.Font, color, center=None, topleft=None):
        surf = font.render(text, True, color)
        rect = surf.get_rect()
        if center is not None:
            rect.center = center
        if topleft is not None:
            rect.topleft = topleft
        self.screen.blit(surf, rect)
        return rect

    # --- Menu --------------------------------------------------------------
    def _menu_difficulty_rects(self) -> list[pygame.Rect]:
        rects = []
        for i in range(len(cfg.DIFFICULTIES)):
            rects.append(pygame.Rect(cfg.WINDOW_WIDTH // 2 - 170, 250 + i * 64, 340, 52))
        return rects

    def _menu_play_rect(self) -> pygame.Rect:
        return pygame.Rect(cfg.WINDOW_WIDTH // 2 - 170, 480, 340, 56)

    def _menu_scores_rect(self) -> pygame.Rect:
        return pygame.Rect(cfg.WINDOW_WIDTH // 2 - 170, 548, 340, 48)

    def _draw_menu(self) -> None:
        self._text("Juego de Memoria", self.font_xl, cfg.COLOR_TEXT,
                   center=(cfg.WINDOW_WIDTH // 2, 120))
        self._text("Elige la dificultad", self.font_md, cfg.COLOR_TEXT_DIM,
                   center=(cfg.WINDOW_WIDTH // 2, 205))

        names = list(cfg.DIFFICULTIES)
        for rect, name in zip(self._menu_difficulty_rects(), names, strict=True):
            selected = name == self.difficulty
            color = cfg.COLOR_ACCENT if selected else cfg.COLOR_PANEL
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            self._text(name, self.font_md, cfg.COLOR_TEXT, center=rect.center)

        play = self._menu_play_rect()
        pygame.draw.rect(self.screen, cfg.COLOR_CARD_MATCHED, play, border_radius=10)
        self._text("JUGAR  (Enter)", self.font_md, cfg.COLOR_TEXT, center=play.center)

        scores = self._menu_scores_rect()
        pygame.draw.rect(self.screen, cfg.COLOR_PANEL, scores, border_radius=10)
        self._text("Mejores puntuaciones  (P)", self.font_sm, cfg.COLOR_TEXT,
                   center=scores.center)

        self._text("Flechas: cambiar  ·  Esc: salir", self.font_sm, cfg.COLOR_TEXT_DIM,
                   center=(cfg.WINDOW_WIDTH // 2, 640))

    # --- Juego -------------------------------------------------------------
    def _draw_playing(self) -> None:
        if self.game is None:
            return
        self._draw_hud()
        for row in range(self.game.board.rows):
            for col in range(self.game.board.cols):
                self._draw_card(row, col)

    def _draw_hud(self) -> None:
        assert self.game is not None
        matched_pairs = sum(1 for c in self.game.board.cards() if c.matched) // 2
        self._text(f"Movimientos: {self.game.moves}", self.font_md, cfg.COLOR_TEXT,
                   topleft=(30, 30))
        secs = int(self.game.elapsed_seconds())
        self._text(f"Tiempo: {secs // 60:02d}:{secs % 60:02d}", self.font_md,
                   cfg.COLOR_TEXT, center=(cfg.WINDOW_WIDTH // 2, 45))
        self._text(f"Parejas: {matched_pairs}/{self.game.board.num_pairs}",
                   self.font_md, cfg.COLOR_TEXT,
                   topleft=(cfg.WINDOW_WIDTH - 230, 30))

    def _draw_card(self, row: int, col: int) -> None:
        assert self.game is not None
        card = self.game.board.card_at(row, col)
        rect = self._card_rect(row, col)
        if card.face_up:
            self.screen.blit(self.images[card.pair_id], rect.topleft)
            border = cfg.COLOR_CARD_MATCHED if card.matched else cfg.COLOR_HIGHLIGHT
            pygame.draw.rect(self.screen, border, rect, width=4, border_radius=8)
        else:
            pygame.draw.rect(self.screen, cfg.COLOR_CARD_BACK, rect, border_radius=8)
            pygame.draw.rect(self.screen, cfg.COLOR_ACCENT, rect, width=2,
                             border_radius=8)
            self._text("?", self.font_lg, cfg.COLOR_CARD_FACE, center=rect.center)

    # --- Overlay de victoria ----------------------------------------------
    def _draw_won_overlay(self) -> None:
        assert self.game is not None
        overlay = pygame.Surface((cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        cx = cfg.WINDOW_WIDTH // 2
        self._text("¡Ganaste!", self.font_xl, cfg.COLOR_HIGHLIGHT, center=(cx, 200))
        secs = int(self.game.elapsed_seconds())
        resumen = f"{self.game.moves} movimientos  ·  {secs // 60:02d}:{secs % 60:02d}"
        self._text(resumen, self.font_md, cfg.COLOR_TEXT, center=(cx, 270))
        self._text("Escribe tu nombre:", self.font_md, cfg.COLOR_TEXT_DIM,
                   center=(cx, 350))

        box = pygame.Rect(cx - 200, 390, 400, 56)
        pygame.draw.rect(self.screen, cfg.COLOR_PANEL, box, border_radius=10)
        pygame.draw.rect(self.screen, cfg.COLOR_ACCENT, box, width=2, border_radius=10)
        caret = "|" if pygame.time.get_ticks() // 500 % 2 == 0 else ""
        self._text(self.name_input + caret, self.font_md, cfg.COLOR_TEXT,
                   center=box.center)
        self._text("Enter para guardar", self.font_sm, cfg.COLOR_TEXT_DIM,
                   center=(cx, 470))

    # --- Tabla de records --------------------------------------------------
    def _draw_scores(self) -> None:
        cx = cfg.WINDOW_WIDTH // 2
        self._text("Top 5 - Mejores puntuaciones", self.font_lg, cfg.COLOR_TEXT,
                   center=(cx, 80))
        top = self.scoreboard.top(5)
        if not top:
            self._text("Aun no hay records. ¡Se el primero!", self.font_md,
                       cfg.COLOR_TEXT_DIM, center=(cx, 300))
        else:
            self._text("#   Nombre            Mov.   Tiempo   Dificultad",
                       self.font_sm, cfg.COLOR_TEXT_DIM, topleft=(120, 160))
            for i, s in enumerate(top, start=1):
                secs = int(s.seconds)
                fila = (f"{i}   {s.name[:14]:<14}   {s.moves:>4}   "
                        f"{secs // 60:02d}:{secs % 60:02d}    {s.difficulty}")
                self._text(fila, self.font_sm, cfg.COLOR_TEXT,
                           topleft=(120, 200 + i * 40))
        self._text("Pulsa cualquier tecla para volver", self.font_sm,
                   cfg.COLOR_TEXT_DIM, center=(cx, 640))


def run() -> None:
    """Crea la aplicacion y arranca el bucle principal."""
    App().run()
