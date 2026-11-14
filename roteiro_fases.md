# Roteiro de Fases e Campanha — Missão Privada

## 1. Sinopse Geral e Ambientação

Em um dia aparentemente comum no campus da **Universidade Federal Fluminense (UFF)**, um silêncio assustador tomou conta dos corredores: os banheiros pararam de funcionar. O que parecia ser apenas mais um problema crônico de encanamento logo revelou uma força sombria. 

Das profundezas esquecidas do subsolo da universidade emergiu o **Gnomo Malvado**, uma criatura rancorosa que encontrou um antigo **Amuleto Místico de Esgoto**. Com ele, o Gnomo passou a canalizar a energia de décadas de dejetos acumulados e sobras esquecidas do Restaurante Universitário (o lendário "bandejão"), dando vida a um exército grotesco: **Cocos mutantes**, **Ratazanas carniceiras** e **Alimentos Podres Zumbis**. O objetivo do Gnomo é provocar o "Grande Transbordamento", inundando todo o campus em uma maré fétida e estabelecendo seu império do lodo.

O único capaz de impedir essa catástrofe sanitária é **Privadus**, o lendário guardião dos encanamentos. Armado com sua coragem, uma resistente **Espada de Desentupidor**, rolos velozes de **Papel Higiênico** e a mística habilidade da **Descarga**, Privadus descerá pelos canos até as entranhas da UFF, cruzará os labirintos do esgoto municipal e invadirá o Super Esgoto para quebrar o amuleto e banir o Gnomo para sempre.

---

## 2. A Mecânica da Seta Amarela e do HUD

### 2.1. Liberdade de Exploração vs. Caminho Canônico
O jogador tem **liberdade total de locomoção**: é possível vagar pelas salas, desviar de inimigos, procurar itens de cura nos cantos e explorar rotas alternativas em qualquer direção. Contudo, cada fase possui uma sequência ordenada de metas chamada de **Caminho Canônico**.

### 2.2. A Seta Amarela Guia
* Em todos os momentos do jogo, uma **pequena seta amarela** é exibida na tela.
* A seta aponta dinamicamente na direção do **próximo passo obrigatório** (calculada pelo ângulo euclidiano entre Privadus e as coordenadas do alvo atual).
* Caso o jogador se afaste ou fuja do caminho para explorar, a seta continua orientando com precisão onde está o próximo ponto de interesse.
* Quando Privadus alcança o objetivo intermediário ou cumpre a condição do passo (ex: derrotar os monstros da sala, coletar uma chave ou ativar um registro), a seta amarela aponta imediatamente para as coordenadas do passo seguinte.

### 2.3. Exibição no HUD
* No canto superior direito, o campo `Objetivo:` reflete o passo imediato em andamento.
* Ao alcançar o último passo da fase, o HUD passa a exibir com destaque o **Objetivo Final da Fase**, que perdura até a transição para a próxima zona.

---

## 3. Roteiro Detalhado das Fases

---

### Fase 1: O Banheiro Assombrado da UFF
* **Zona:** 1ª Zona — Estrutura da UFF (Parte 1).
* **Ambientação:** O banheiro masculino do bloco central da UFF. Ladrilhos brancos encardidos, torneiras pingando, poças suspeitas no chão e portas de cabines entreabertas.
* **O que acontece:** Privadus acorda trancado no banheiro após ouvir ruídos estranhos de borbulhas. Os ralos começam a expelir lama tóxica e surgem os primeiros Cocos perseguidores. Privadus precisa se rearmar, coletar suprimentos de papel higiênico, inspecionar a encanação e acionar a privada encantada para abrir a rota subterrânea de manutenção.

#### Conjunto de Passos a Seguir (Trilha da Seta Amarela):
1. **Passo 1 (Despertar e Defesa):** Seguir até a cabine 3 no canto superior esquerdo e pegar o *Desentupidor Reforçado* encostado na parede.
2. **Passo 2 (Munição Sanitária):** Seguir até o dispenser quebrado na parede norte para coletar um estoque inicial de *Papel Higiênico Projetil*.
3. **Passo 3 (Primeira Limpeza):** Eliminar a patrulha de 3 Cocos menores que emergiu do ralo central perto das pias.
4. **Passo 4 (Alívio de Pressão):** Ir até a válvula vermelha na tubulação da parede direita e pressionar `E` para despressurizar os canos do setor.
5. **Passo 5 (Acesso Secreto):** Caminhar até o Vaso Sanitário Mágico no canto inferior esquerdo (ao lado da divisória de metal).
6. **Passo 6 (Transição):** Pressionar `E` junto ao vaso para acionar a Descarga e ser sugado diretamente para os dutos de ventilação inferiores.

* **Texto do Objetivo Final da Fase no HUD:**
  > `Objetivo: Dar a descarga no vaso principal e descer pelo cano`

---

### Fase 2: As Galerias de Manutenção da UFF
* **Zona:** 1ª Zona — Estrutura da UFF (Parte 2).
* **Ambientação:** Corredores subterrâneos estreitos, cabos de rede suspensos, paredes de concreto bruto e depósitos esquecidos de arquivos e móveis velhos.
* **O que acontece:** O cheiro de decomposição piora drasticamente. Aqui, os restos descartados do bandejão da UFF foram reanimados pela magia do amuleto, transformando-se em Alimentos Podres Zumbis que emitem radiação fétida contínua. No centro do bloco das caldeiras, o primeiro tenente do Gnomo aguarda: o temível **Rei Coco**. Privadus precisa religar os geradores, drenar o porão e vencer o chefe para obter a chave do esgoto público.

#### Conjunto de Passos a Seguir (Trilha da Seta Amarela):
1. **Passo 1 (Avanço Cauteloso):** Percorrer o corredor estreito leste mantendo distância segura da aura dos Zumbis de Bandejão.
2. **Passo 2 (Energia de Emergência):** Ir até a caixa de disjuntores no almoxarifado de ferramentas e acionar a chave geral para iluminar as galerias.
3. **Passo 3 (Bomba Hidráulica):** Seguir até o mezanino das bombas e puxar a alavanca para sugar o lodo que bloqueava a porta da caldeira.
4. **Passo 4 (Enfrentamento do Chefe):** Entrar na câmara da caldeira central, onde o **Rei Coco** cai do teto com estrondo.
5. **Passo 5 (Eliminação):** Destruir os minions que o Rei Coco invoca e desferir golpes nele até esgotar seu HP.
6. **Passo 6 (Coleta e Fuga):** Coletar a *Chave Mestra da Grelha Sanitária* que o Rei Coco derruba e abrir o alçapão enferrujado no chão da sala.

* **Texto do Objetivo Final da Fase no HUD:**
  > `Objetivo: Derrotar o Rei Coco e abrir a comporta do esgoto`

---

### Fase 3: O Labirinto de Galerias Fétidas
* **Zona:** 2ª Zona — Sistema de Esgoto (Parte 1).
* **Ambientação:** A rede pública de esgoto da cidade de Niterói. Layouts labirínticos simulando canos cilíndricos gigantes, passarelas escorregadias de madeira e rios caudalosos de detritos escuros.
* **O que acontece:** O terreno torna-se traiçoeiro e amplo. Ratazanas rápidas emboscam Privadus pelas sombras, preparando botes em velocidade tripla (*hit-and-run*). Para avançar, Privadus precisa desobstruir três comportas mecânicas que regulam o fluxo das águas e impedem o acesso ao reservatório principal.

#### Conjunto de Passos a Seguir (Trilha da Seta Amarela):
1. **Passo 1 (Desafio da Passarela):** Avançar pela ponte de madeira do canal sul esquivando dos botes das Ratazanas de esgoto.
2. **Passo 2 (Comporta Ocidental):** Encontrar a primeira manivela hidráulica no cano oeste e girá-la para fechar o vazamento de esgoto bruto.
3. **Passo 3 (Kit de Desentupimento Profundo):** Localizar no abrigo dos operários uma caixa contendo o upgrade temporário de *Desinfetante Concentrado* (aumento de dano de tiro).
4. **Passo 4 (Comporta Oriental):** Atravessar a ponte metálica superior e acionar a segunda manivela para baixar o nível da água na encruzilhada.
5. **Passo 5 (Desobstrução do Duto):** Usar o ataque de Descarga para afastar a barricada de cocos presos na entrada da galeria mestra.
6. **Passo 6 (Portão do Reservatório):** Seguir até o arco de tijolos maciços que guarda a entrada do Reservatório Central.

* **Texto do Objetivo Final da Fase no HUD:**
  > `Objetivo: Drenar o labirinto e acessar o Reservatório Central`

---

### Fase 4: O Reservatório Tóxico da Ratazana Gigante
* **Zona:** 2ª Zona — Sistema de Esgoto (Parte 2).
* **Ambientação:** Uma gigantesca abóbada subterrânea circular, sustentada por pilares de pedra secular tomados pelo limo. No chão, poças de ácido verde venenoso e canos despejando dejetos industriais.
* **O que acontece:** O santuário da **Ratazana Gigante**, a criatura mutante que lidera as pragas urbanas. Com agilidade extrema, ela salta de parede em parede, ricocheteando pelas bordas da tela e deixando rastros permanentes de veneno. Privadus precisa antecipar sua trajetória, manobrar no espaço limitado e derrotá-la para recuperar o mapa de acesso ao Super Esgoto.

#### Conjunto de Passos a Seguir (Trilha da Seta Amarela):
1. **Passo 1 (Reconhecimento da Arena):** Descer as escadarias de ferro até o platô central de pedra seca.
2. **Passo 2 (Isca Sanitária):** Posicionar uma pastilha sanitária aromática no pedestal central para atrair a fera.
3. **Passo 3 (Confronto com a Fera):** Esquivar das investidas ricocheteantes da Ratazana Gigante e não pisar nas poças tóxicas estáticas criadas por ela.
4. **Passo 4 (Ataque a Distância):** Usar os projéteis de Papel Higiênico e a repulsão da Descarga quando ela encurralar Privadus na borda da tela.
5. **Passo 5 (Derrota da Fera):** Aplicar o golpe final com a Espada de Desentupidor quando a fera estafar.
6. **Passo 6 (O Salto Abissal):** Coletar o *Lacre de Selênio* do chão e saltar na correnteza do vertedouro que despenca rumo ao Super Esgoto.

* **Texto do Objetivo Final da Fase no HUD:**
  > `Objetivo: Eliminar a Ratazana Gigante e mergulhar no vertedouro profundo`

---

### Fase 5: O Santuário do Lodo Proibido
* **Zona:** 3ª Zona — Esconderijo do Gnomo / Super Esgoto (Parte 1).
* **Ambientação:** Uma cidadela ancestral subterrânea sob as rochas da Baía de Guanabara, esculpida em pedra vulcânica e esgoto cristalizado. Runas místicas brilhantes iluminam colunas colossais, e a água escorre em sentido inverso pelas paredes.
* **O que acontece:** Privadus invade o perímetro de segurança do Gnomo Malvado. As forças inimigas agora operam sob feitiçaria pura: Cocos blindados por escudos de lodo e sentinelas arcanas. Três altares de contenção protegem os portões do trono do Gnomo; Privadus precisa quebrar as três pedras rúnicas nos três cantos do santuário.

#### Conjunto de Passos a Seguir (Trilha da Seta Amarela):
1. **Passo 1 (Invasão do Santuário):** Atravessar o portal de rocha quebrando a formação de Cocos arcanos.
2. **Passo 2 (Runa do Mau Cheiro):** Ir até a ala oeste do templo e golpear a pedra rúnica verde até destruí-la (desativando o veneno passivo da sala).
3. **Passo 3 (Travessia das Ilhas de Sabão):** Pular entre as plataformas flutuantes sobre o abismo negro de dejetos.
4. **Passo 4 (Runa da Corrupção):** Ir até a ala leste do templo e quebrar a pedra rúnica roxa (cessando o surgimento contínuo de zumbis).
5. **Passo 5 (A Runa Central):** Voltar ao pórtico principal e usar o impacto total da habilidade Descarga na runa dourada que lacra o portal.
6. **Passo 6 (Rumo ao Trono):** Cruzar o portão aberto da cidadela em direção à arena do confronto final.

* **Texto do Objetivo Final da Fase no HUD:**
  > `Objetivo: Destruir as 3 Runas Arcanas e abrir o portal do Trono do Gnomo`

---

### Fase 6: O Super Esgoto — O Confronto Final contra o Gnomo
* **Zona:** 3ª Zona — Esconderijo do Gnomo / Super Esgoto (Parte 2).
* **Ambientação:** Uma arena colossal suspensa sobre um turbilhão cósmico de água escura. Ao fundo, engrenagens titânicas e canos banhados a ouro. No centro, sobre uma privada monumental dourada, o **Gnomo Malvado** levita envolto por um brilho ametista emanado do amuleto.
* **O que acontece:** A batalha suprema pelo destino da universidade e da cidade. O Gnomo revela seu poder total em um combate dinâmico de *Bullet Hell*, disparando rajadas geométricas calculadas de projéteis mágicos em espirais e estrelas. Privadus precisa de reflexos afiados, precisão de movimento e o domínio total de suas armas para destruir o amuleto e puxar a Descarga Suprema que purificará todo o sistema.

#### Conjunto de Passos a Seguir (Trilha da Seta Amarela):
1. **Passo 1 (Início do Duelo):** Caminhar até o círculo ritualístico no coração da arena para desafiar o Gnomo.
2. **Passo 2 (Sobrevivência à Espiral Arcana):** Desviar da 1ª onda de rajadas em espiral calculadas com trigonometria circular disparadas pelo amuleto.
3. **Passo 3 (Sobrecarga dos Tubos de Água):** A seta aponta para as válvulas laterais da arena; acione ambas para lançar jatos d'água sob alta pressão e romper o escudo mágico do chefe.
4. **Passo 4 (Fase Crítica de Bullet Hell):** Com HP abaixo de 50%, o Gnomo ataca com rajadas triplas cruzadas e investidas de Cocos teleguiados. Utilizar os i-frames e a repulsão da Descarga para abrir brechas seguras de tiro.
5. **Passo 5 (Golpe no Amuleto):** Quando o Gnomo ficar atordoado após a sobrecarga, aproximar-se e acertar um ataque certeiro com o desentupidor direto no amuleto místico.
6. **Passo 6 (A Descarga Suprema):** A seta amarela aponta para a majestosa Corrente de Ouro da Descarga Imperial. Interagir com ela (`tecla E`) para banir o Gnomo, purificar todo o esgoto e restaurar a paz na UFF.

* **Texto do Objetivo Final da Fase no HUD:**
  > `Objetivo: Derrotar o Gnomo Malvado e puxar a Descarga Suprema`

---

## 4. Tabela Resumo da Campanha e Objetivos do HUD

| Fase | Nome da Fase | Ambiente / Zona | Inimigos & Ameaças | Alvo da Seta Amarela Final | Texto do Objetivo Final no HUD |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | **O Banheiro Assombrado** | Banheiro da UFF (Zona 1) | Cocos menores | Vaso Sanitário Mágico | `Dar a descarga no vaso principal e descer pelo cano` |
| **2** | **Galerias de Manutenção** | Porão e Caldeiras (Zona 1) | Alimentos Podres & **Rei Coco** | Alçapão do Chão | `Derrotar o Rei Coco e abrir a comporta do esgoto` |
| **3** | **Labirinto de Galerias Fétidas** | Rede de Tubulações (Zona 2) | Ratazanas (*hit-and-run*) | Portão de Tijolos | `Drenar o labirinto e acessar o Reservatório Central` |
| **4** | **O Reservatório Tóxico** | Abóbada Alagada (Zona 2) | Poças de Veneno & **Ratazana Gigante** | Vertedouro Abissal | `Eliminar a Ratazana Gigante e mergulhar no vertedouro profundo` |
| **5** | **Santuário do Lodo Proibido** | Cidadela Arcana (Zona 3) | Cocos Blindados & Zumbis Arcanos | Portal do Trono | `Destruir as 3 Runas Arcanas e abrir o portal do Trono do Gnomo` |
| **6** | **O Trono do Super Esgoto** | Arena Final Cósmica (Zona 3) | Projéteis Mágicos & **Gnomo Malvado** | Corrente de Ouro | `Derrotar o Gnomo Malvado e puxar a Descarga Suprema` |

---

## 5. Diretrizes Técnicas de Implementação no Código

Para integrar o roteiro às classes do projeto de forma limpa e desacoplada:

1. **Gestor de Passos (`StepManager` ou Lista de Waypoints na `Phase`):**
   * Cada fase define sua lista sequencial de passos: `steps = [{"description": str, "target_pos": (x, y), "trigger_type": "reach" | "interact" | "defeat_boss"}, ...]`.
   * Um índice `__current_step_index` rastreia o progresso da fase.
2. **Atualização da Seta Amarela (`YellowArrow`):**
   * Posicionada próxima ao contorno de Privadus ou na borda da tela.
   * Ângulo calculado dinamicamente em tempo real:
     $$\theta = \text{atan2}(y_{\text{alvo}} - y_{\text{jogador}}, x_{\text{alvo}} - x_{\text{jogador}})$$
   * Desenha o sprite da seta rotacionado em $\theta$ graus apontando para o alvo do passo atual.
3. **Sincronização com o `Hud`:**
   * Enquanto `__current_step_index < total_passos - 1`, o HUD recebe:
     `hud.set_objective(passo_atual["description"])`.
   * Quando o jogador atinge a etapa decisiva da fase, o HUD recebe:
     `hud.set_objective(fase.OBJETIVO_FINAL)`.
   * A progressão respeita a independência de taxa de quadros com `delta_time` e o padrão de encapsulamento `POO-01` e `POO-02`.
