# Documento de Design Técnico: Missão Privada

## 1. Arquitetura e Configurações Base
*   **Engine/Tecnologia:** Python 3.x com a biblioteca **PPlay** (extensão do Pygame).
*   **Estrutura do Game Loop:** O jogo rodará dentro de um loop principal contínuo padrão do PPlay, utilizando `window = Window(largura, altura)`. O controle de velocidade de todas as entidades deve obrigatoriamente ser multiplicado por `window.delta_time()` para garantir consistência de movimento independente de framerate.
*   **Resolução e Renderização:** 
    *   Resolução base da janela sugerida: 1280x720 ou 1920x1080.
    *   Como a arte é em Pixel Art focada em formas simples, as imagens (`Sprite`) devem ser escalonadas previamente ou via código sem filtros de suavização para não embaçar os pixels.
*   **Controles (Inputs) via `window.get_keyboard()` e `window.get_mouse()`:**
    *   **Movimento:** Teclas WASD ou Setas. O vetor de movimento precisa ser normalizado no código Python para que o personagem não ande mais rápido nas diagonais.
    *   **Ataque Básico:** Botão Esquerdo do Mouse.
    *   **Habilidade/Ataque Secundário:** Botão Direito do Mouse.
    *   **Interação (Cenário):** Tecla 'E'.
    *   **Dash/Esquiva:** Tecla Espaço.

## 2. Sistema de Mapas e Geração
Como o PPlay não possui um sistema de mapas (Tilemaps) nativo complexo como outras engines, a geração procedural será tratada via matrizes (arrays bidimensionais) no Python.
*   **Matriz de Grade (Grid):** O mapa será lido a partir de matrizes de números inteiros, onde cada número representa um bloco (ex: 0 = chão livre, 1 = parede/cano, 2 = obstáculo interativo).
*   **Renderização de Cenário:** Iterar sobre a matriz e desenhar `GameImage` ou `Sprite` na tela com base na posição `(linha * tamanho_tile, coluna * tamanho_tile)`.
*   **Regiões da Run:**
    *   1ª Zona (Estrutura da UFF): Corredores estreitos e salas retangulares.
    *   2ª Zona (Sistema de esgoto): Layouts labirínticos simulando canos e galerias.
    *   3ª Zona (Esconderijo do gnomo - super esgoto): Arenas amplas para focar nas batalhas contra chefes.
*   **Transição:** Ao derrotar o chefe (boss), o PPlay carrega a matriz da próxima fase e reposiciona o `Sprite` do jogador nas coordenadas iniciais da nova sala.

## 3. Componentes de Gameplay e Entidades
Todas as entidades do jogo serão classes Python que herdam ou encapsulam a classe `Sprite` do PPlay.

**3.1. O Jogador (Privadus)**
*   **Classe `Player`:** Gerencia o `Sprite` do Privadus, HP, velocidade base e controle de frames de invulnerabilidade (i-frames utilizando contadores baseados no `delta_time`).
*   **Colisão:** Checagem de física utilizando o método `privadus_sprite.collided(obstaculo_sprite)`. A lógica de deslizar na parede (sliding) precisará ser implementada separadamente, separando a checagem de colisão do eixo X e do eixo Y.

**3.2. Inteligência Artificial dos Inimigos**
Implementada através de uma Máquina de Estados Finitos (FSM) dentro do método `update()` de cada classe de inimigo:
*   **Cocos (Swarm):** Utilizam lógica simples de perseguição geométrica. Calculam o vetor direção entre a posição do coco e a posição de Privadus, movendo-se em linha reta até ele causando dano de contato.
*   **Ratazanas de esgoto (Hit and Run):** Máquina de estados alternando entre `patrulha_aleatoria`, `carregar_ataque` (espera 1 segundo) e `investida_rapida` (aumenta a velocidade em 3x na direção do jogador).
*   **Alimentos podres zumbis (Tanks/AoE):** Andam lentamente. Emitem dano em área, verificado checando a distância euclidiana `math.dist(pos_zumbi, pos_player)` para aplicar dano contínuo caso o jogador esteja no raio de efeito.

**3.3. Sistema de Chefes (Boss Fights)**
Classes específicas herdando de inimigos base, porém com métodos adicionais para **Fases** de ataque (acionadas quando o HP cai abaixo de certos limiares).
*   **Rei Coco:** Método `spawn_minions()` que instancia objetos da classe Coco no array de inimigos ativos da tela.
*   **Ratazana Gigante:** Lógica de ricochetear pelas bordas da tela (`x <= 0`, `x >= limite_tela`, etc.) e instanciar `Sprites` de poças de veneno estáticas.
*   **Gnomo Malvado (Boss Final):** Sistema de *Bullet Hell*. O Gnomo possui um array de projéteis e um temporizador para disparar múltiplos `Sprites` em ângulos matematicamente calculados (usando seno e cosseno no Python) a partir do amuleto.

## 4. Sistema de Builds e Roguelike
O jogo necessita de um sistema modular para lidar com o aspecto temporário das melhorias (perdidas ao fim da run).
*   **Gerenciador de Status (`StatManager`):** Um dicionário ou classe no jogador que guarda os modificadores atuais (ex: `self.dano_extra`, `self.velocidade_projétil`). Ao final de cada run, esses valores são resetados para o padrão.
*   **Itens de Chão:** `Sprites` espalhados pelo mapa que, ao colidirem com o jogador, executam funções como recuperar HP.
*   **Armas e Modificadores:**
    *   *Espada de desentupidor:* Cria um `Sprite` de hit-box invisível (ou com animação) rapidamente na frente do jogador quando o mouse é clicado.
    *   *Lançadores de papel higiênico:* Cria instâncias de uma classe `Projetil` que se move na direção do clique do mouse, checando colisão iterativamente contra a lista de inimigos.
    *   *Descarga:* Habilidade de área de efeito. Aplica uma força inversa aos inimigos próximos e os afasta (fórmula de repulsão alterando as coordenadas `x` e `y` dos inimigos).

## 5. Interface de Usuário (UI)
A interface será desenhada sempre no final do loop de renderização (após desenhar o mapa e os personagens), para ficar sobreposta a todos os elementos.
*   **Vida e Recursos:** Utilização das ferramentas nativas do PPlay para desenhar barras (retângulos coloridos cujo tamanho da base altera proporcionalmente ao HP) ou desenhando múltiplos `Sprites` de "coraçãozinho".
*   **Textos (Informações da Run):** O método `window.draw_text()` será utilizado no canto superior direito para exibir o tempo de sobrevivência, estágio atual e objetivos.

## 6. Sistema de Áudio e Feedback
*   **PPlay Sound:** O áudio será gerido pelas classes de som nativas da biblioteca.
*   **Trilha Sonora (BGM):** Um arquivo tocando em loop (método `play()` com parâmetro de repetição).
*   **Efeitos Sonoros (SFX):** Efeitos curtos (tiros de papel higiênico, inimigos recebendo dano) carregados na memória.
*   **Som da Descarga (Feedback Especial):** Ao usar a habilidade "Descarga", além do som em alto volume, o jogo pode aplicar um leve efeito de *Screen Shake* (vibração de câmera), implementado aplicando um pequeno deslocamento randômico (via `random.randint` do Python) nas coordenadas de desenho (offset) de todos os itens do cenário e inimigos por meio segundo.