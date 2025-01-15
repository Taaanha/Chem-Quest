import pygame
import os
import random
import sys
import textwrap
import math

pygame.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Chem Quest")

FLAME_COLORS = {
    "Li": (220, 20, 60),        # Crimson red
    "Na": (255, 255, 0),        # Bright yellow
    "K": (216, 191, 216),       # Lilac
    "Rb": (199, 21, 133),       # Red-violet
    "Cs": (138, 43, 226),       # Blue-violet
    "Fr": (255, 69, 0)          # Orange-red
}

background = pygame.image.load(r"E:\\python\\reaction\\flame test\\candle.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

jar_image = pygame.image.load(r"E:\\python\\reaction\\flame test\\file (2).png")
jar_image = pygame.transform.scale(jar_image, (150, 190))

element_images = {
    "Li": pygame.image.load(r"E:\\python\\reaction\\flame test\\Lithium.png"),
    "Na": pygame.image.load(r"E:\\python\\reaction\\flame test\\Na.png"),
    "K": pygame.image.load(r"E:\\python\\reaction\\flame test\\k.png"),
    "Rb": pygame.image.load(r"E:\\python\\reaction\\flame test\\Rb.png"),
    "Cs": pygame.image.load(r"E:\\python\\reaction\\flame test\\Cs.png"),
    "Fr": pygame.image.load(r"E:\\python\\reaction\\flame test\\Fr.png"),
}

for key in element_images:
    element_images[key] = pygame.transform.scale(element_images[key], (50, 50))

# Jar positions
jar_positions = [(150 + i * 170, SCREEN_HEIGHT - 200) for i in range(6)]
labels = ["Li", "Na", "K", "Rb", "Cs", "Fr"]


font_path = r"E:\python\map\Berthany.otf"
font = pygame.font.Font(font_path, 70) 
label_font = pygame.font.Font(font_path, 35) 


class FlameParticle:
    alpha_layer_qty = 2
    alpha_glow_difference_constant = 2

    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.original_r = r
        self.color = color
        self.alpha_layers = FlameParticle.alpha_layer_qty
        self.alpha_glow = FlameParticle.alpha_glow_difference_constant
        max_surf_size = 2 * self.r * self.alpha_layers * self.alpha_layers * self.alpha_glow
        self.surf = pygame.Surface((max_surf_size, max_surf_size), pygame.SRCALPHA)
        self.burn_rate = 0.1 * random.randint(1, 4)

    def update(self):
        self.y -= 7 - self.r
        self.x += random.randint(-self.r, self.r)
        self.original_r -= self.burn_rate
        self.r = int(self.original_r)
        if self.r <= 0:
            self.r = 1

    def draw(self):
        max_surf_size = 2 * self.r * self.alpha_layers * self.alpha_layers * self.alpha_glow
        self.surf = pygame.Surface((max_surf_size, max_surf_size), pygame.SRCALPHA)
        for i in range(self.alpha_layers, -1, -1):
            alpha = 255 - i * (255 // self.alpha_layers - 5)
            if alpha <= 0:
                alpha = 0
            radius = self.r * i * i * self.alpha_glow
            color = (*self.color, alpha)
            pygame.draw.circle(
                self.surf, color, (self.surf.get_width() // 2, self.surf.get_height() // 2), radius
            )
        screen.blit(self.surf, self.surf.get_rect(center=(self.x, self.y)))


class Flame:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.flame_particles = []
        self.color = (255, 140, 0)  

    def set_color(self, color):
        self.color = color

    def update(self):
        for particle in self.flame_particles:
            particle.update()
        self.flame_particles = [p for p in self.flame_particles if p.r > 1]

        for _ in range(5):
            self.flame_particles.append(
                FlameParticle(
                    self.x + random.randint(-10, 10),
                    self.y,
                    random.randint(3, 7),
                    self.color,
                )
            )

    def draw(self):
        for particle in self.flame_particles:
            particle.draw()



class Element:
    def __init__(self, label, x, y):
        self.label = label
        self.image = element_images[label]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.original_pos = self.rect.topleft
        self.dragging = False

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

    def update(self, pos):
        if self.dragging:
            self.rect.center = pos

    def reset_position(self):
        self.rect.topleft = self.original_pos



elements = [Element(label, jar_positions[i][0] + (150 // 2) - 25, jar_positions[i][1] + (190 // 2) - 25) 
            for i, label in enumerate(labels)]


label_vertical_offset = 160 

def flame_test_colors_game():
    running = True
    dragged_element = None
    reaction_result = ""

    flame = Flame(790, SCREEN_HEIGHT - 542)  

 
    exit_button = pygame.Rect(SCREEN_WIDTH - 80, 10, 60, 60)

    
    reaction_messages = {
        "Li": "produces Crimson red color in the flame test!",
        "Na": "produces Bright yellow color in the flame test!",
        "K": "produces Lilac color in the flame test!",
        "Rb": "produces Red-violet color in the flame test!",
        "Cs": "produces Blue-violet color in the flame test!",
        "Fr": "produces Orange-red color in the flame test!"
    }

    while running:
        screen.blit(background, (0, 0))

      
        title_text = font.render("Flame Test", True, (255, 255, 255))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))

       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if exit_button.collidepoint(event.pos): 
                        running = False

                    for element in elements:
                        if element.rect.collidepoint(event.pos):
                            element.dragging = True
                            dragged_element = element
                            break

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: 
                    if dragged_element:
                        if flame.x - 50 <= event.pos[0] <= flame.x + 50 and flame.y - 50 <= event.pos[1] <= flame.y + 50:
                            flame.set_color(FLAME_COLORS[dragged_element.label])
                            reaction_result = dragged_element.label  
                        dragged_element.dragging = False
                        dragged_element.reset_position()
                        dragged_element = None

            if event.type == pygame.MOUSEMOTION:
                if dragged_element:
                    dragged_element.update(event.pos)

     
        for label, (x, y) in zip(labels, jar_positions):
            screen.blit(jar_image, (x, y))

        for element in elements:
            element.draw()

        
        for i, label in enumerate(labels):
            label_text = label_font.render(label, True, (255, 255, 255))
            screen.blit(label_text, (jar_positions[i][0] + (150 // 2) - label_text.get_width() // 2, jar_positions[i][1] + label_vertical_offset))

        
        flame.update()
        flame.draw()

      
        pygame.draw.rect(screen, (139, 69, 19), exit_button)  
        cross_text = font.render("X", True, (255, 255, 255))
        screen.blit(cross_text, (exit_button.centerx - cross_text.get_width() // 2, exit_button.centery - cross_text.get_height() // 2))

        if reaction_result:
           
            element_text = font.render(reaction_result, True, (255, 255, 255))
            screen.blit(element_text, (50, 100))

           
            message_text = font.render(reaction_messages[reaction_result], True, (255, 255, 255))
            screen.blit(message_text, (50 + element_text.get_width() + 10, 100)) 

        pygame.display.flip()
        pygame.time.Clock().tick(60)

map_image = pygame.image.load("E:\\python\\map\\Map.png")
map_image = pygame.transform.scale(map_image, screen.get_size())  


kingdom_images = [
    pygame.image.load("E:\\python\\map\\alkile.webp"),
    pygame.image.load("E:\\python\\map\\alkaline.jpg"),
    pygame.image.load("E:\\python\\map\\noble gas.webp"),
    pygame.image.load("E:\\python\\map\\metal.jpg"),
    pygame.image.load("E:\\python\\map\\halogen.webp"),
    pygame.image.load("E:\\python\\map\\lantha ide.webp"),
]

game_button_images = {
    0: [
        pygame.image.load("E:\\python\\map\\vol0b.png"),
        pygame.image.load("E:\\python\\map\\vol1b.png"),
        pygame.image.load("E:\\python\\map\\vol2b.png"),
        pygame.image.load("E:\\python\\map\\vol3b.png"),
    ],
    1: [
        pygame.image.load("E:\\python\\map\\albut0.png"),
        pygame.image.load("E:\\python\\map\\albut1.png"),
        pygame.image.load("E:\\python\\map\\albut2.png"),
        pygame.image.load("E:\\python\\map\\albut3.png"),
    ],
    2: [
        pygame.image.load("E:\\python\\map\\nobut0.png"),
        pygame.image.load("E:\\python\\map\\nobut1.png"),
        pygame.image.load("E:\\python\\map\\nobut2.png"),
        pygame.image.load("E:\\python\\map\\nobut3.png"),
    ],
    3: [
        pygame.image.load("E:\\python\\map\\metalbut0.png"),
        pygame.image.load("E:\\python\\map\\metalbut1.png"),
    ],
    4: [
        pygame.image.load("E:\\python\\map\\h0b.png"),
        pygame.image.load("E:\\python\\map\\h1b.png"),
        pygame.image.load("E:\\python\\map\\h2b.png"),
        pygame.image.load("E:\\python\\map\\h3b.png"),
    ],
    5: [
        pygame.image.load("E:\\python\\map\\c0b (2).png"),
        pygame.image.load("E:\\python\\map\\c1b.png"),
        pygame.image.load("E:\\python\\map\\c2b.png"),
    ],
}


map_width, map_height = map_image.get_size()
clickable_areas = [
    pygame.Rect(map_width * 0.10, map_height * 0.2, map_width * 0.2, map_height * 0.15),  # Area 1
    pygame.Rect(map_width * 0.4, map_height * 0.1, map_width * 0.2, map_height * 0.15),  # Area 2
    pygame.Rect(map_width * 0.8, map_height * 0.1, map_width * 0.2, map_height * 0.15),  # Area 3
    pygame.Rect(map_width * 0.3, map_height * 0.4, map_width * 0.2, map_height * 0.15),  # Area 4
    pygame.Rect(map_width * 0.5, map_height * 0.6, map_width * 0.2, map_height * 0.15),  # Area 5
    pygame.Rect(map_width * 0.8, map_height * 0.6, map_width * 0.2, map_height * 0.15),  # Area 6
]


def handle_click(position):
    for i, area in enumerate(clickable_areas):
        if area.collidepoint(position):
            display_image_and_games(i)  
            break


def display_image_and_games(index):
    running = True

  
    screen_width, screen_height = screen.get_size()
    button_width = screen_width // 5  
    button_height = screen_height // 3 
    gap = 20  

   
    if index == 3:  # Metal kingdom
        num_buttons = 2
    elif index == 5:  # Lanthanide kingdom
        num_buttons = 3
    else:
        num_buttons = 4  # Default for other kingdoms

    start_x = (screen_width - (num_buttons * button_width + (num_buttons - 1) * gap)) // 2  
    y_position = (screen_height - button_height) // 2  

    button_positions = [
        pygame.Rect(start_x + i * (button_width + gap), y_position, button_width, button_height)
        for i in range(num_buttons)
    ]

    while running:
        screen.fill((0, 0, 0)) 
        screen.blit(kingdom_images[index], (0, 0))  

        
        for i, rect in enumerate(button_positions):
            button_image = pygame.transform.scale(game_button_images[index][i], (button_width, button_height))
            screen.blit(button_image, rect.topleft)

       
        back_button = pygame.Rect(50, 50, 200, 60)  
        pygame.draw.rect(screen, (139, 69, 19), back_button)  
        back_font = pygame.font.Font(None, 36)
        back_text = back_font.render("Back to Map", True, (255, 255, 255))  
        text_x = back_button.x + (back_button.width - back_text.get_width()) // 2
        text_y = back_button.y + (back_button.height - back_text.get_height()) // 2
        screen.blit(back_text, (text_x, text_y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    running = False
                for i, rect in enumerate(button_positions):
                    if rect.collidepoint(event.pos):
                        print(f"Game {i + 1} selected in Kingdom {index + 1}!")  # Debug
                        run_game(index + 1, i + 1)
def alkali_metals_sorting_game():
   
    pygame.init()

    
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Alkali Metals Sorting Mini-Game")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (100, 149, 237)
    GREEN = (34, 139, 34)
    RED = (220, 20, 60)
    DARK_BROWN = (101, 67, 33)

    berthany_font = pygame.font.Font("E:\\python\\Berthany.otf", 48)  
    element_font = berthany_font  

    background = pygame.image.load("E:\\python\\drag and match\\bg.webp")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    correct_sound = pygame.mixer.Sound("E:\\python\\correct_sound.wav.wav")

   
    properties = [
        {
            "name": "Reactivity with Water",
            "order": ["Fr", "Cs", "Rb", "K", "Na", "Li"],
            "instruction": "Arrange the elements in order of decreasing reactivity, starting with the most reactive and ending with the least reactive.",
            "explanation": "Reactivity increases down the group. Francium reacts most violently, while Lithium reacts gently."
        },
      {
        "name": "Atomic Radius",
        "order": ["Fr", "Cs", "Rb", "K", "Na", "Li"],
        "instruction": "Arrange the elements in order of decreasing atomic radius, starting with the largest and ending with the smallest.",
        "explanation": "Atomic radius increases down the group due to the addition of electron shells."
    },
    {
        "name": "Melting Point",
        "order": ["Li", "Na", "K", "Rb", "Cs", "Fr"],
        "instruction": "Arrange the elements in order of decreasing melting points, starting with the highest and ending with the lowest.",
        "explanation": "Melting points decrease as you move down Group 1. The metallic bonds become weaker with increasing atomic size."
    },
    {
        "name": "Boiling Point",
        "order": ["Li", "Na", "K", "Rb", "Cs", "Fr"],
        "instruction": "Arrange the elements in order of decreasing boiling points, starting with the highest and ending with the lowest.",
        "explanation": "Boiling points decrease as you move down Group 1 because the metallic bonds become weaker with increasing atomic size and lower attraction between atoms."
    },
    {
        "name": "Ionization Energy",
        "order": ["Li", "Na", "K", "Rb", "Cs", "Fr"],
        "instruction": "Arrange the elements in order of decreasing ionization energy, starting with the highest and ending with the lowest.",
        "explanation": "Ionization energy decreases as you move down Group 1. The outermost electron is farther from the nucleus and experiences less nuclear attraction, making it easier to remove."
    },
    {
        "name": "Electronegativity",
        "order": ["Li", "Na", "K", "Rb", "Cs", "Fr"],
        "instruction": "Arrange the elements in order of decreasing electronegativity, starting with the highest and ending with the lowest.",
        "explanation": "Electronegativity decreases as you move down Group 1. Larger atoms have a reduced ability to attract shared electrons in a bond due to increased distance from the nucleus."
    },
    {
        "name": "Hydration Enthalpy",
        "order": ["Li", "Na", "K", "Rb", "Cs", "Fr"],
        "instruction": "Arrange the elements in order of decreasing hydration enthalpy, starting with the highest and ending with the lowest.",
        "explanation": "Hydration enthalpy decreases as you move down Group 1. Smaller ions, like Li⁺, have a higher charge density and interact more strongly with water molecules compared to larger ions."
    },
    {
        "name": "Density",
        "order": ["Fr", "Cs", "Rb", "K", "Na", "Li"],
        "instruction": "Arrange the elements in order of decreasing density, starting with the highest and ending with the lowest.",
        "explanation": "Density generally decreases as you move up Group 1. Although atomic volume increases as you move down the group, the overall mass of the atom has a greater influence, leading to higher densities lower in the group. Francium is the densest alkali metal."
    }
    ]

   
    current_property_index = 0
    current_property = properties[current_property_index]
    elements = [
        {"name": metal, "rect": pygame.Rect(WIDTH // 2 - 300 + i * 120, HEIGHT // 2 - 25, 100, 50), "dragging": False, "placed": False, "correct": False, "speed": [random.choice([-1, 1]), random.choice([-1, 1])]} 
        for i, metal in enumerate(current_property["order"])
    ]
    targets = [
        pygame.Rect(WIDTH // 2 - 300 + i * 120, HEIGHT // 2 + 100, 100, 50)
        for i in range(len(current_property["order"]))
    ]


    exit_button = pygame.Rect(WIDTH - 60, 10, 50, 50)

    def draw_background():
        """Draw the game background."""
        screen.blit(background, (0, 0))

    def draw_elements():
        """Draw draggable elements."""
        for element in elements:
            color = GREEN if element["correct"] else (RED if element["placed"] else DARK_BROWN)
            pygame.draw.rect(screen, color, element["rect"])
            text = element_font.render(element["name"], True, WHITE)
            text_rect = text.get_rect(center=element["rect"].center)
            screen.blit(text, text_rect)

    def draw_targets():
        """Draw target areas."""
        for i, target in enumerate(targets):
            pygame.draw.rect(screen, RED, target, 2)

    def draw_instructions_and_explanation():
        """Draw instructions and explanations for the current property."""
        instruction_lines = textwrap.wrap(current_property["instruction"], width=60)
        explanation_lines = textwrap.wrap(current_property["explanation"], width=60)

      
        instruction_texts = [berthany_font.render(line, True, WHITE) for line in instruction_lines]
        explanation_texts = [berthany_font.render(line, True, WHITE) for line in explanation_lines]

      
        instruction_y_offset = HEIGHT // 8
        explanation_y_offset = HEIGHT - (HEIGHT // 8)  

       
        for i, text in enumerate(instruction_texts):
            text_rect = text.get_rect(center=(WIDTH // 2, instruction_y_offset + i * 60))
            screen.blit(text, text_rect)
        
       
        for i, text in enumerate(explanation_texts):
            text_rect = text.get_rect(center=(WIDTH // 2, explanation_y_offset + i * 60))
            screen.blit(text, text_rect)

    def move_elements():
        """Move elements around the screen."""
        for element in elements:
            if not element["dragging"] and not element["placed"]:
                element["rect"].x += element["speed"][0]
                element["rect"].y += element["speed"][1]

                if element["rect"].left < 0 or element["rect"].right > WIDTH:
                    element["speed"][0] *= -1
                if element["rect"].top < 0 or element["rect"].bottom > HEIGHT:
                    element["speed"][1] *= -1

    def check_completion():
        """Check if the elements are sorted correctly."""
        for i, element in enumerate(elements):
            if not targets[i].collidepoint(element["rect"].center) or not element["correct"]:
                return False
        return True

  
    running = True
    while running:
        screen.fill(WHITE)
        draw_background()
        move_elements()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            # Handle mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos): 
                    running = False

                for element in elements:
                    if element["rect"].collidepoint(event.pos) and not element["placed"]:
                        element["dragging"] = True

            elif event.type == pygame.MOUSEBUTTONUP:
                for i, element in enumerate(elements):
                    if element["dragging"]:
                        element["dragging"] = False
                        if targets[i].collidepoint(element["rect"].center):
                            if element["name"] == current_property["order"][i]:
                                element["rect"].center = targets[i].center
                                element["placed"] = True
                                element["correct"] = True
                                correct_sound.play() 
                            else:
                                element["placed"] = True
                                element["correct"] = False

            elif event.type == pygame.MOUSEMOTION:
                for element in elements:
                    if element["dragging"]:
                        element["rect"].x += event.rel[0]
                        element["rect"].y += event.rel[1]

       
        draw_elements()
        draw_targets()
        draw_instructions_and_explanation()

        
        pygame.draw.rect(screen, (139, 69, 19), exit_button)  
        cross_text = berthany_font.render("X", True, (255, 255, 255))
        screen.blit(cross_text, (exit_button.centerx - cross_text.get_width() // 2, exit_button.centery - cross_text.get_height() // 2))

        
        if check_completion():
            current_property_index += 1
            if current_property_index >= len(properties):
                print("Game completed!")
                running = False
            else:
                current_property = properties[current_property_index]
                elements = [
                    {"name": metal, "rect": pygame.Rect(WIDTH // 2 - 300 + i * 120, HEIGHT // 2 - 25, 100, 50), "dragging": False, "placed": False, "correct": False, "speed": [random.choice([-1, 1]), random.choice([-1, 1])]} 
                    for i, metal in enumerate(current_property["order"])
                ]

       
        pygame.display.flip()

   
    pygame.quit()
    sys.exit()
def alkaline_info():
   
    pygame.init()

    
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Alkaline Earth Metals Info")
 
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    SKY_BLUE = (135, 206, 250)
    RED = (255, 0, 0)


    content_font = pygame.font.Font("E:\\python\\Berthany.otf", 36)
    button_font = pygame.font.Font(None, 36)

    background = pygame.image.load("E:\\python\\map\\alkaline.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

   
    content = {
        "Introduction": "Alkaline earth metals are elements in Group 2 of the periodic table. "
                        "They are less reactive than alkali metals but still form compounds readily.",
        "Details": "1. Found in Group 2 of the periodic table.\n"
                   "2. Includes beryllium, magnesium, calcium, strontium, barium, and radium.\n"
                   "3. Shiny, silvery-white metals with two valence electrons.\n"
                   "4. Moderately reactive, especially with acids and water.",
        "Important Information": "1. They are harder and have higher melting points compared to alkali metals.\n"
                                  "2. Reactivity increases as you move down the group.\n"
                                  "3. Compounds like calcium carbonate (limestone) are vital in construction and biological processes.\n"
                                  "4. Radium is radioactive and found in trace amounts in uranium ores.",
        "Storage and Safety": "1. Alkaline earth metals should be stored in sealed containers or inert environments to prevent oxidation.\n"
                              "2. Magnesium and calcium should be kept away from moisture to avoid corrosion.\n"
                              "3. Always handle strontium, barium, and radium with caution due to their reactivity or radioactivity.",
        "Usage": "1. Magnesium is used in lightweight alloys and fire-starting tools.\n"
                 "2. Calcium is vital for bone health, cement production, and steel refining.\n"
                 "3. Strontium is used in fireworks and flares for its bright red color.\n"
                 "4. Barium is used in medical imaging and as a drilling fluid additive.",
        "Fun Facts": "1. Magnesium burns with an intensely bright white flame.\n"
                     "2. Calcium is the fifth most abundant element in the Earth's crust.\n"
                     "3. Strontium compounds were used historically in signal rockets.\n"
                     "4. Radium, once used in luminous paint, was later discontinued due to its radioactivity."
    }

  
    scroll_offset = 0
    scroll_speed = 10
    padding = 20  

  
    wrapped_lines = []
    for section, text in content.items():
        wrapped_lines.append(f"{section}:")
        wrapped_lines.extend(textwrap.wrap(text, width=70))
        wrapped_lines.append("")  

   
    line_height = content_font.size("A")[1]
    content_width = max(content_font.size(line)[0] for line in wrapped_lines) + 2 * padding
    content_height = len(wrapped_lines) * line_height + 2 * padding

   
    box_width = min(content_width, WIDTH - 100)
    box_height = min(content_height, HEIGHT - 100)
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2

    
    button_width, button_height = 50, 30
    button_x, button_y = WIDTH - button_width - 10, 10
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

   
    running = True
    while running:
        screen.blit(background, (0, 0))

        
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(screen, SKY_BLUE, box_rect)
        pygame.draw.rect(screen, BLACK, box_rect, 2)

        
        pygame.draw.rect(screen, RED, button_rect)
        text_surface = button_font.render("X", True, WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_DOWN:
                    scroll_offset = min(scroll_offset + scroll_speed, max(0, content_height - box_height + padding))
                elif event.key == pygame.K_UP:
                    scroll_offset = max(scroll_offset - scroll_speed, 0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False

       
        y = box_y + padding - scroll_offset
        for line in wrapped_lines:
            if y + line_height > box_y + padding and y < box_y + box_height - padding:
                text_surface = content_font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, y + line_height // 2))
                screen.blit(text_surface, text_rect)
            y += line_height

        
        pygame.display.flip()
def alflame():
    pygame.init()
   
    FLAME_COLORS = {
        "Be": None,                   # No color change
        "Mg": (255, 255, 255),        # Bright white
        "Ca": (255, 140, 0),          # Orange-red
        "Sr": (220, 20, 60),          # Crimson red
        "Ba": (124, 252, 0),          # Green
        "Ra": (173, 216, 230)         # Pale blue (hypothetical)
    }

    background = pygame.image.load(r"E:\\python\\map\\alkaline\\flametest\\Untitled design (6).png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    jar_image = pygame.image.load(r"E:\\python\\reaction\\flame test\\file (2).png")
    jar_image = pygame.transform.scale(jar_image, (150, 190))

    element_images = {
        "Be": pygame.image.load(r"E:\\python\\map\\alkaline\\flametest\\Be.png"),
        "Mg": pygame.image.load(r"E:\\python\\map\\alkaline\\flametest\\Mg.png"),
        "Ca": pygame.image.load(r"E:\\python\\map\\alkaline\\flametest\\Ca.png"),
        "Sr": pygame.image.load(r"E:\\python\\map\\alkaline\\flametest\\Sr.png"),
        "Ba": pygame.image.load(r"E:\\python\\map\\alkaline\\flametest\\Ba.png"),
        "Ra": pygame.image.load(r"E:\\python\map\\alkaline\\flametest\\Ra.png"),
    }

    for key in element_images:
        element_images[key] = pygame.transform.scale(element_images[key], (50, 50))

   
    jar_positions = [(150 + i * 170, SCREEN_HEIGHT - 200) for i in range(6)]
    labels = ["Be", "Mg", "Ca", "Sr", "Ba", "Ra"]

    font_path = r"E:\\python\\Berthany.otf"
    font = pygame.font.Font(font_path, 60)  
    label_font = pygame.font.Font(font_path, 40)  

   
    class FlameParticle:
        alpha_layer_qty = 2
        alpha_glow_difference_constant = 2

        def __init__(self, x, y, r, color):
            self.x = x
            self.y = y
            self.r = r
            self.original_r = r
            self.color = color
            self.alpha_layers = FlameParticle.alpha_layer_qty
            self.alpha_glow = FlameParticle.alpha_glow_difference_constant
            max_surf_size = 2 * self.r * self.alpha_layers * self.alpha_layers * self.alpha_glow
            self.surf = pygame.Surface((max_surf_size, max_surf_size), pygame.SRCALPHA)
            self.burn_rate = 0.1 * random.randint(1, 4)

        def update(self):
            self.y -= 7 - self.r
            self.x += random.randint(-self.r, self.r)
            self.original_r -= self.burn_rate
            self.r = int(self.original_r)
            if self.r <= 0:
                self.r = 1

        def draw(self):
            max_surf_size = 2 * self.r * self.alpha_layers * self.alpha_layers * self.alpha_glow
            self.surf = pygame.Surface((max_surf_size, max_surf_size), pygame.SRCALPHA)
            for i in range(self.alpha_layers, -1, -1):
                alpha = 255 - i * (255 // self.alpha_layers - 5)
                if alpha <= 0:
                    alpha = 0
                radius = self.r * i * i * self.alpha_glow
                color = (*self.color, alpha)
                pygame.draw.circle(
                    self.surf, color, (self.surf.get_width() // 2, self.surf.get_height() // 2), radius
                )
            screen.blit(self.surf, self.surf.get_rect(center=(self.x, self.y)))


    class Flame:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.flame_particles = []
            self.color = (255, 140, 0) 

        def set_color(self, color):
            self.color = color

        def update(self):
            for particle in self.flame_particles:
                particle.update()
            self.flame_particles = [p for p in self.flame_particles if p.r > 1]

            for _ in range(5):
                self.flame_particles.append(
                    FlameParticle(
                        self.x + random.randint(-10, 10),
                        self.y,
                        random.randint(3, 7),
                        self.color,
                    )
                )

        def draw(self):
            for particle in self.flame_particles:
                particle.draw()


   
    class Element:
        def __init__(self, label, x, y):
            self.label = label
            self.image = element_images[label]
            self.rect = self.image.get_rect(topleft=(x, y))
            self.original_pos = self.rect.topleft
            self.dragging = False

        def draw(self):
            screen.blit(self.image, self.rect.topleft)

        def update(self, pos):
            if self.dragging:
                self.rect.center = pos

        def reset_position(self):
            self.rect.topleft = self.original_pos


    elements = [Element(label, jar_positions[i][0] + (150 // 2) - 25, jar_positions[i][1] + (190 // 2) - 25) 
                for i, label in enumerate(labels)]

    
    label_vertical_offset = 160  

    
    reaction_messages = {
        "Be": '"Be" produces no distinctive color in the flame test!',
        "Mg": '"Mg" produces Bright white color in the flame test!',
        "Ca": '"Ca" produces Orange-red color in the flame test!',
        "Sr": '"Sr" produces Crimson color in the flame test!',
        "Ba": '"Ba" produces Apple Green color in the flame test!',
        "Ra": ('"Ra" is a radioactive element and is not typically used in flame tests. '
               'due to its extreme radioactivity and potential health hazards. '
               'We can assume a pale blue hypothetically.')
    }

    running = True
    dragged_element = None
    reaction_result = ""

   
    flame = Flame(770, SCREEN_HEIGHT - 400)

    exit_button = pygame.Rect(SCREEN_WIDTH - 60, 10, 50, 50)

    while running:
        screen.blit(background, (0, 0))

        
        title_text = font.render("Flame Test", True, (255, 255, 255))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if exit_button.collidepoint(event.pos):
                        running = False
                    for element in elements:
                        if element.rect.collidepoint(event.pos):
                            element.dragging = True
                            dragged_element = element
                            break

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if dragged_element:
                        if flame.x - 50 <= event.pos[0] <= flame.x + 50 and flame.y - 50 <= event.pos[1] <= flame.y + 50:
                            if FLAME_COLORS[dragged_element.label]:
                                flame.set_color(FLAME_COLORS[dragged_element.label])
                            reaction_result = reaction_messages.get(dragged_element.label, "")
                        dragged_element.dragging = False
                        dragged_element.reset_position()
                        dragged_element = None

            if event.type == pygame.MOUSEMOTION:
                if dragged_element:
                    dragged_element.update(event.pos)

        
        for label, (x, y) in zip(labels, jar_positions):
            screen.blit(jar_image, (x, y))

        for element in elements:
            element.draw()

        
        for i, label in enumerate(labels):
            label_text = label_font.render(label, True, (255, 255, 255))
            screen.blit(label_text, (jar_positions[i][0] + (150 // 2) - label_text.get_width() // 2, jar_positions[i][1] + label_vertical_offset))

       
        flame.update()
        flame.draw()

       
        pygame.draw.rect(screen, (139, 69, 19), exit_button)
        cross_font = pygame.font.Font(None, 36)
        cross_text = cross_font.render("X", True, (255, 255, 255))
        screen.blit(cross_text, (exit_button.centerx - cross_text.get_width() // 2, exit_button.centery - cross_text.get_height() // 2))

        
        if reaction_result:
            if len(reaction_result) > 80:
                lines = reaction_result.split('. ')
                for i, line in enumerate(lines):
                    result_text = font.render(line, True, (255, 255, 255))
                    screen.blit(result_text, (50, 100 + i * 50))
            else:
                result_text = font.render(reaction_result, True, (255, 255, 255))
                screen.blit(result_text, (50, 100))

        pygame.display.update()
def radioactive_maze_game():

    pygame.init()


    SCREEN_WIDTH = 1600
    SCREEN_HEIGHT = 900
    CELL_SIZE = 40
    MAZE_WIDTH = SCREEN_WIDTH // CELL_SIZE
    MAZE_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
    GIFTS_COUNT = 3

   
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Radioactive Maze")


    background_image = pygame.image.load(r"E:\python\map\alkaline\Ra Maze\bg.webp").convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    brick_image = pygame.image.load(r"E:\python\map\alkaline\Ra Maze\brickk.png").convert()
    brick_image = pygame.transform.scale(brick_image, (CELL_SIZE, CELL_SIZE))
    obstacle_image = pygame.image.load(r"E:\python\map\alkaline\Ra Maze\Ra.png").convert_alpha()
    obstacle_image = pygame.transform.scale(obstacle_image, (CELL_SIZE, CELL_SIZE))
    exit_image = pygame.image.load(r"E:\python\map\alkaline\Ra Maze\Exitt.png").convert_alpha()
    exit_image = pygame.transform.scale(exit_image, (CELL_SIZE, CELL_SIZE))
    player_image = pygame.image.load(r"E:\python\map\alkaline\Ra Maze\playerr.png").convert_alpha()
    player_image = pygame.transform.scale(player_image, (CELL_SIZE, CELL_SIZE))
    gift_image = pygame.image.load(r"E:\python\map\alkaline\Ra Maze\Box.png").convert_alpha()
    gift_image = pygame.transform.scale(gift_image, (CELL_SIZE, CELL_SIZE))
    cross_image = pygame.image.load(r"E:\python\map\alkaline\Ra Maze\back.png").convert_alpha()
    cross_image = pygame.transform.scale(cross_image, (50, 50))

    
    font_path = r"E:\python\Berthany.otf"
    big_font = pygame.font.Font(font_path, 72)
    small_font = pygame.font.Font(font_path, 36)
    knowledge_font = pygame.font.Font(font_path, 40)

  
    game_over_sound = pygame.mixer.Sound(r"E:\python\map\alkaline\Ra Maze\game-over-39-199830.mp3")
    game_win_sound = pygame.mixer.Sound(r"E:\python\map\alkaline\Ra Maze\game-bonus-144751.mp3")
    box_collect_sound = pygame.mixer.Sound(r"E:\python\map\alkaline\Ra Maze\correct_sound.wav.wav")

    
    knowledge_list = [ "Radium was once considered so valuable and mysterious that it was called 'liquid sunshine' and inspired many products, including the infamous 'Radithor,' a radioactive tonic.",
    "Radium emits ionizing radiation, which can damage cells and DNA, leading to serious health consequences.",
    "A famous case highlighting the dangers of radium involved the 'Radium Girls,' factory workers who suffered severe health issues from painting watch dials with radium paint and licking brushes to maintain precision.",
    "Prolonged exposure to radium can cause radiation sickness, burns, anemia, bone fractures, and cancer.",
    "Radium was once included in health products like toothpaste, water, and even beauty creams, marketed as a 'miracle cure.'",
    "It was used in early cancer treatments (radiotherapy) and to shrink tumors due to its ability to emit radiation.",
    "In the early 20th century, radium was used in luminous paints for clocks, watches, and aircraft instruments.",
    "Radium is a highly radioactive element, emitting alpha particles, beta particles, and gamma rays during its decay.",
    "Radium is a silvery-white metal that glows faintly in the dark due to its radioactivity. It turns black when exposed to air.",
    "Radium decays to radon gas, which is also radioactive and can pose health risks.",
    "Radium was discovered by Marie Curie and Pierre Curie in 1898 while researching pitchblende ore (a type of uranium ore).",
    "The name 'radium' is derived from the Latin word 'radius,' meaning 'ray,' reflecting its radioactive properties.",
    "Marie Curie received two Nobel Prizes, one for Physics in 1903 (shared with Pierre Curie and Henri Becquerel) and another for Chemistry in 1911 for her work on radium and polonium."]

    
    def create_maze():
        maze = [[0] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]
        
        
        shapes = [
         [
    (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), 
    (4,2),(5,2),(6,2),(7,2),(8,2),(9,2),(10,2),(11,2),(12,2),(13,2),(14,2),
    (5, 5), (4, 6), (3, 6), (2, 6), (1, 6), 
    (5, 6), (6, 5), (7, 5), (8, 5), (9, 5), 
    (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), 
    (7, 11), (7, 12), (7, 13), (7, 14), (7, 15), 
    (7, 16), (7, 5), (7, 4)
],


[
    (5, 20), (5, 21), (8, 16), (8, 17), (8, 18), 
    (8, 19), (8, 20), (8, 21), (8, 22), (9, 17), 
    (10, 17), (11, 17), (12, 17), (13, 17), (14, 17), 
    (15, 17), (15, 16), (15, 15), (15, 14), (15, 13), 
    (15, 12), (16, 12), (17, 12), (18, 12), (18, 13), 
    (18, 14), (18, 15), (18, 16), (18, 17), (18, 18), 
    (19, 18), (20, 18), (21, 18), (22, 18)
],

# Reverse Large L shape
[
    (10, 10), (11, 10), (12, 10), 
    (10, 11), (10, 12)
],

# Large C shape
[
    (15, 5), (16, 5), (17, 5), 
    (15, 6), (15, 7), 
    (17, 6), (17, 7)
],

# Reverse Large C shape
[
    (20, 10), (21, 10), (22, 10), 
    (22, 11), (22, 12), (22, 13), (22, 14),
    (22, 15), (22, 16), (22, 17), (22, 18),
    (23,15),(24,15),(24,16),(24,17),(24,18),
    (25,15),(26,15),(27,15),(28,15),(29,15),(30,15),(31,15),(32,15),(33,15),(34,15),(35,15),
    (35,16),(35,17),(35,18),(35,19),(35,20),
    (36,16),(36,17),(37,16),
    (20, 11), (20, 12)
],

# Another Reverse Large C shape
[
    (30, 10), (31, 10), (32, 10), 
    (32, 11), (32, 12), 
    (30, 11), (30, 12)
],

# T shape
[
    (19, 5), (20, 5), (21, 5), (22, 5), (23, 5), 
    (24, 5), (24,4),(24,3),(24,2),(25, 5), (26, 5), (27, 5), (28, 5), 
    (29, 5), (30, 5), (31, 5), (32, 5), (33, 5), 
    (26, 6), (26, 7), (26, 8), (26, 9), (26, 10), 
    (26, 11), (26, 12), (25, 24), (25, 23), (25, 22)
],

# Reverse T shape
[
    (30, 10), (31, 10), (32, 10), (33, 10), (34, 10), 
    (31, 9), (31, 8), (31, 7), (31, 6)
],

# J shape
[
    (35, 5), (36, 5), (37, 5), 
    (37, 6), (37, 7)
],

# Reverse J shape
[
    (40, 10), (41, 10), (42, 10), 
    (40, 11), (40, 12), (40, 13), (40, 14), (40, 15), (40, 16), (40, 17), (40, 18), (40, 19),(40,20),
]

        ]
        
        
        for shape in shapes:
            for (dx, dy) in shape:
                if 0 <= dx < MAZE_WIDTH and 0 <= dy < MAZE_HEIGHT:
                    maze[dy][dx] = 1

    
        radium_positions = [
            (3,3),(4,9),(5,10),(7,13),(9,15),(7,26),
        (8, 5), (40, 5), (30, 19), (27, 9), (28,14),
        (9, 5), (28, 7), (10, 8), (11, 15), (15, 5),
        (27, 6), (11, 10), (26, 12), (18, 7), (18,11),
        (11, 13), (9, 14), (10, 15), (11, 18), (12, 20),(18,10),
        (5, 15), (15, 10), (5, 17), (18, 20), (6, 17),
        (10, 20), (19, 23), (12, 16), (10, 21), (10, 22),(15,15),
        (15, 25), (16, 25), (17, 25), (16, 26), (16, 27),
        (20, 30), (21, 30), (22, 30), (21, 29), (21, 28),
        (25, 35), (26, 35), (27, 35),(27,8), (27, 36), (27, 37),(25,2),(25,18),(22,20),(18,19),(26,5),(25,2),(32,20),(25,6),(40,18),(40,10),
        (30, 40), (31, 40), (32, 40), (30, 41), (30, 42),(45,5),
        ]

        for (rx, ry) in radium_positions:
            if 0 <= rx < MAZE_WIDTH and 0 <= ry < MAZE_HEIGHT:
                maze[ry][rx] = 3

       
        maze[MAZE_HEIGHT - 1][MAZE_WIDTH - 1] = 2
        return maze

    # Maze
    def draw_maze(screen, maze):
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                if maze[y][x] == 1:
                    screen.blit(brick_image, (x * CELL_SIZE, y * CELL_SIZE))
                elif maze[y][x] == 2:
                    screen.blit(exit_image, (x * CELL_SIZE, y * CELL_SIZE))
                elif maze[y][x] == 3:
                    screen.blit(obstacle_image, (x * CELL_SIZE, y * CELL_SIZE))

    # Player class
    class Player:
        def __init__(self):
            self.x = 0
            self.y = 0

        def move(self, dx, dy, maze):
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT and maze[new_y][new_x] != 1 and maze[new_y][new_x] != 3:
                self.x = new_x
                self.y = new_y

        def draw(self, screen):
            screen.blit(player_image, (self.x * CELL_SIZE, self.y * CELL_SIZE))

    # Timer class
    class Timer:
        def __init__(self, countdown_time):
            self.font = pygame.font.SysFont("E:\\python\\Berthany.otf", 36)
            self.start_time = pygame.time.get_ticks()
            self.countdown_time = countdown_time  # Time in seconds

        def get_time(self):
            elapsed_time = pygame.time.get_ticks() - self.start_time
            remaining_time = self.countdown_time - elapsed_time // 1000
            if remaining_time < 0:
                remaining_time = 0
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            return f"Time: {minutes:02}:{seconds:02}"

        def draw(self, screen):
            time_text = self.font.render(self.get_time(), True, WHITE)
            screen.blit(time_text, (10, SCREEN_HEIGHT - 40))

        def is_time_up(self):
            elapsed_time = pygame.time.get_ticks() - self.start_time
            remaining_time = self.countdown_time - elapsed_time // 1000
            return remaining_time <= 0

    def start_screen():
        screen.blit(background_image, (0, 0))
        title_text = big_font.render("Radioactive Maze", True, WHITE)
        rules_text1 = small_font.render("Avoid Radiums and Escape the maze within 1 min!", True, WHITE)
        rules_text2 = small_font.render("Collect the gift boxes for knowledge gifts!", True, WHITE)
        start_text = small_font.render("Press ENTER to Start", True, WHITE)
        
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))
        screen.blit(rules_text1, (SCREEN_WIDTH // 2 - rules_text1.get_width() // 2, SCREEN_HEIGHT // 4 + 100))
        screen.blit(rules_text2, (SCREEN_WIDTH // 2 - rules_text2.get_width() // 2, SCREEN_HEIGHT // 4 + 150))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(cross_image, (SCREEN_WIDTH - 60, 10))  # Draw cross-shaped exit button
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if SCREEN_WIDTH - 60 <= event.pos[0] <= SCREEN_WIDTH - 10 and 10 <= event.pos[1] <= 60:
                            return False

        return True

    def end_screen(message):
        screen.blit(background_image, (0, 0))
        end_text = big_font.render(message, True, WHITE)
        screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, SCREEN_HEIGHT // 2 - end_text.get_height() // 2))
        screen.blit(cross_image, (SCREEN_WIDTH - 60, 10))  # Draw cross-shaped exit button
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if SCREEN_WIDTH - 60 <= event.pos[0] <= SCREEN_WIDTH - 10 and 10 <= event.pos[1] <= 60:
                            return False

    def display_gifts():
        screen.blit(background_image, (0, 0))
        gift_positions = [(SCREEN_WIDTH // 4 * i, SCREEN_HEIGHT // 2) for i in range(1, 4)]
        for pos in gift_positions:
            screen.blit(gift_image, pos)
        screen.blit(cross_image, (SCREEN_WIDTH - 60, 10))  # Draw cross-shaped exit button
        pygame.display.flip()
        
        collected_knowledge = random.sample(knowledge_list, 3)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if SCREEN_WIDTH - 60 <= event.pos[0] <= SCREEN_WIDTH - 10 and 10 <= event.pos[1] <= 60:
                            return False
                        clicked_gift_index = (event.pos[0] // (SCREEN_WIDTH // 4)) - 1
                        if 0 <= clicked_gift_index < len(collected_knowledge):
                            box_collect_sound.play()
                            display_knowledge(collected_knowledge[clicked_gift_index])
                            collected_knowledge.pop(clicked_gift_index)
                            if not collected_knowledge:
                                waiting = False

    def display_knowledge(knowledge):
        screen.blit(background_image, (0, 0))
        lines = []
        words = knowledge.split()
        line = ''
        for word in words:
            if knowledge_font.size(line + word)[0] < SCREEN_WIDTH - 40:
                line += word + ' '
            else:
                lines.append(line)
                line = word + ' '
        lines.append(line)

        y_offset = SCREEN_HEIGHT // 2 - len(lines) * knowledge_font.get_height() // 2
        for line in lines:
            knowledge_text = knowledge_font.render(line, True, WHITE)
            screen.blit(knowledge_text, (SCREEN_WIDTH // 2 - knowledge_text.get_width() // 2, y_offset))
            y_offset += knowledge_font.get_height()
        screen.blit(cross_image, (SCREEN_WIDTH - 60, 10))  # Draw cross-shaped exit button
        pygame.display.flip()
        pygame.time.wait(5000)  # Give enough time to read

    # Main game loop
    def main():
        if not start_screen():
            return  # Exit if the start screen returns False

        font = pygame.font.SysFont("E:\\python\\Berthany.otf", 36)
        clock = pygame.time.Clock()
        maze = create_maze()
        player = Player()
        countdown_time = 60  # Countdown time in seconds (1 minute)
        timer = Timer(countdown_time)
        running = True
        won = False
        game_over = False

        # Place gift boxes randomly in the maze
        gift_positions = []
        for _ in range(GIFTS_COUNT):
            while True:
                x = random.randint(0, MAZE_WIDTH - 1)
                y = random.randint(0, MAZE_HEIGHT - 1)
                if maze[y][x] == 0 and (x, y) not in gift_positions and (x, y) != (0, 0) and (x, y) != (MAZE_WIDTH - 1, MAZE_HEIGHT - 1):
                    gift_positions.append((x, y))
                    break

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return  # Exit game loop if quit event is triggered
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player.move(0, -1, maze)
                    elif event.key == pygame.K_DOWN:
                        player.move(0, 1, maze)
                    elif event.key == pygame.K_LEFT:
                        player.move(-1, 0, maze)
                    elif event.key == pygame.K_RIGHT:
                        player.move(1, 0, maze)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if SCREEN_WIDTH - 60 <= event.pos[0] <= SCREEN_WIDTH - 10 and 10 <= event.pos[1] <= 60:
                            return  # Exit game loop if exit button is clicked

            screen.blit(background_image, (0, 0))
            draw_maze(screen, maze)
            player.draw(screen)
            timer.draw(screen)

            # Draw gift boxes
            for pos in gift_positions:
                screen.blit(gift_image, (pos[0] * CELL_SIZE, pos[1] * CELL_SIZE))

            # Check if player has collected a gift
            if (player.x, player.y) in gift_positions:
                gift_positions.remove((player.x, player.y))
                box_collect_sound.play()
            
            
            if maze[player.y][player.x] == 3:
                game_over = True
                running = False
            
           
            if maze[player.y][player.x] == 2:
                won = True
                running = False

           
            if timer.is_time_up():
                game_over = True
                running = False

            pygame.display.flip()
            clock.tick(30)

       
        if won:
            if not gift_positions:
                game_win_sound.play()
                display_gifts()
            else:
                game_win_sound.play()
                end_screen('You won! But missed some gifts.')
        elif game_over:
            game_over_sound.play()
            end_screen('Player died from Radiation')
        else:
            game_over_sound.play()
            end_screen('Time is up!')

    main()
def alkaline_earth_metals_sorting_game():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Alkaline Earth Metals Sorting Mini-Game")
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (100, 149, 237)
    GREEN = (34, 139, 34)
    RED = (220, 20, 60)
    BABY_BLUE = (137, 207, 240)
    instruction_font = pygame.font.Font("E:\\python\\Berthany.otf", 40)
    element_font = pygame.font.Font(None, 36)
    background = pygame.image.load("E:\\python\\map\\alkaline\\dnm\\alkaline.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    correct_sound = pygame.mixer.Sound("E:\\python\\map\\alkaline\\dnm\\correct_sound.wav.wav")
    properties = [
        {
            "name": "Reactivity with Water",
            "order": ["Ra", "Ba", "Sr", "Ca", "Mg", "Be"],
            "instruction": "Arrange the elements in order of decreasing reactivity, starting with the most reactive and ending with the least reactive.",
            "explanation": "Reactivity increases down the group. Radium reacts most vigorously, while Beryllium reacts the least."
        },
        {
            "name": "Atomic Radius",
            "order": ["Ra", "Ba", "Sr", "Ca", "Mg", "Be"],
            "instruction": "Arrange the elements in order of decreasing atomic radius, starting with the largest and ending with the smallest.",
            "explanation": "Atomic radius increases down the group due to the addition of electron shells."
        },
        {
            "name": "Melting Point",
            "order": ["Be", "Mg", "Ca", "Sr", "Ba", "Ra"],
            "instruction": "Arrange the elements in order of decreasing melting points, starting with the highest and ending with the lowest.",
            "explanation": "Melting points generally decrease as you move down Group 2. Metallic bonds weaken with increasing atomic size."
        },
        {
            "name": "Density",
            "order": ["Ra", "Ba", "Sr", "Be", "Ca", "Mg"],
            "instruction": "Arrange the elements in order of decreasing density, starting with the highest and ending with the lowest.",
            "explanation": "While density tends to increase down the group, anomalies exist. Beryllium has a higher density than Magnesium and Calcium due to its compact atomic structure."
        }
    ]
    current_property_index = 0
    current_property = properties[current_property_index]
    elements = [
        {"name": metal, "rect": pygame.Rect(WIDTH // 2 - 300 + i * 120, HEIGHT // 2 - 25, 100, 50), "dragging": False, "placed": False, "correct": False, "speed": [random.choice([-1, 1]), random.choice([-1, 1])]} 
        for i, metal in enumerate(current_property["order"])
    ]
    targets = [
        pygame.Rect(WIDTH // 2 - 300 + i * 120, HEIGHT // 2 + 100, 100, 50)
        for i in range(len(current_property["order"]))
    ]

    def draw_background():
        """Draw the game background."""
        screen.blit(background, (0, 0))

    def draw_elements():
        """Draw draggable elements."""
        for element in elements:
            color = GREEN if element["correct"] else (RED if element["placed"] else BABY_BLUE)
            pygame.draw.rect(screen, color, element["rect"])
            text = element_font.render(element["name"], True, WHITE)
            text_rect = text.get_rect(center=element["rect"].center)
            screen.blit(text, text_rect)

    def draw_targets():
        """Draw target areas."""
        for i, target in enumerate(targets):
            pygame.draw.rect(screen, RED, target, 2)

    def draw_instructions_and_explanation():
        """Draw instructions and explanations for the current property."""
        instruction_lines = textwrap.wrap(current_property["instruction"], width=60)
        explanation_lines = textwrap.wrap(current_property["explanation"], width=60)
        instruction_y = 50 
        for i, line in enumerate(instruction_lines):
            instruction_text = instruction_font.render(line, True, WHITE)
            instruction_text_rect = instruction_text.get_rect(center=(WIDTH // 2, instruction_y + i * 40))
            screen.blit(instruction_text, instruction_text_rect)
        explanation_y = HEIGHT - 150  
        for i, line in enumerate(explanation_lines):
            explanation_text = instruction_font.render(line, True, WHITE)
            explanation_text_rect = explanation_text.get_rect(center=(WIDTH // 2, explanation_y + i * 40))
            screen.blit(explanation_text, explanation_text_rect)

    def move_elements():
        """Move elements around the screen."""
        for element in elements:
            if not element["dragging"] and not element["placed"]:
                element["rect"].x += element["speed"][0]
                element["rect"].y += element["speed"][1]

                if element["rect"].left < 0 or element["rect"].right > WIDTH:
                    element["speed"][0] *= -1
                if element["rect"].top < 0 or element["rect"].bottom > HEIGHT:
                    element["speed"][1] *= -1

    def check_completion():
        """Check if the elements are sorted correctly."""
        for i, element in enumerate(elements):
            if not targets[i].collidepoint(element["rect"].center) or not element["correct"]:
                return False
        return True
    running = True
    while running:
        screen.fill(WHITE)
        draw_background()
        move_elements()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for element in elements:
                    if element["rect"].collidepoint(event.pos) and not element["placed"]:
                        element["dragging"] = True

            elif event.type == pygame.MOUSEBUTTONUP:
                for i, element in enumerate(elements):
                    if element["dragging"]:
                        element["dragging"] = False
                        if targets[i].collidepoint(element["rect"].center):
                            if element["name"] == current_property["order"][i]:
                                element["rect"].center = targets[i].center
                                element["placed"] = True
                                element["correct"] = True
                                correct_sound.play()  
                            else:
                                element["placed"] = True
                                element["correct"] = False

            elif event.type == pygame.MOUSEMOTION:
                for element in elements:
                    if element["dragging"]:
                        element["rect"].x += event.rel[0]
                        element["rect"].y += event.rel[1]
        draw_elements()
        draw_targets()
        draw_instructions_and_explanation()
        if check_completion():
            current_property_index += 1
            if current_property_index >= len(properties):
                print("Game completed!")
                running = False
            else:
                current_property = properties[current_property_index]
                elements = [
                    {"name": metal, "rect": pygame.Rect(WIDTH // 2 - 300 + i * 120, HEIGHT // 2 - 25, 100, 50), "dragging": False, "placed": False, "correct": False, "speed": [random.choice([-1, 1]), random.choice([-1, 1])]} 
                    for i, metal in enumerate(current_property["order"])
                ]

    
        pygame.display.flip()
    pygame.quit()
    sys.exit()
def run_noble_gas_info():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Noble Gas Info")
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    SKY_BLUE = (135, 206, 250)
    RED = (255, 0, 0)
    content_font = pygame.font.Font("E:\\python\\Berthany.otf", 36)
    button_font = pygame.font.Font("E:\\python\\Berthany.otf", 36)

    
    background = pygame.image.load("E:\\python\\map\\noble gas.webp")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    content = {
        "Introduction": "Noble gases are a group of elements in Group 18 of the periodic table. "
                        "They are known for their stability and inert nature due to their full valence electron shell.",
        "Details": "1. Found in Group 18 of the periodic table.\n"
                   "2. Colorless, odorless, tasteless gases.\n"
                   "3. Low boiling and melting points.\n"
                   "4. Very low chemical reactivity.\n"
                   "5. Helium, the lightest noble gas, is vital for applications requiring extreme cold.",
        "Important Information": "1. Discovered in the 19th century by Sir William Ramsay.\n"
                                  "2. Helium is commonly used in weather balloons due to its low density and inertness.\n"
                                  "3. Radon, the noble gas with the highest atomic number, is radioactive and can pose health hazards.\n"
                                  "4. Argon is the noble gas most commonly used in light bulbs, preventing filament oxidation.",
        "Usage": "1. Helium is used in balloons, cryogenics, and MRI machines.\n"
                 "2. Neon is famous for its use in advertising signs, creating vibrant red and orange colors.\n"
                 "3. Argon is widely used in welding and industrial processes due to its inert nature.\n"
                 "4. Xenon is essential for high-performance lighting, such as car headlamps and plasma TVs.",
        "Fun Facts": "1. Krypton and argon gases enhance energy efficiency in windows.\n"
                     "2. Radon, though radioactive, was historically used in medical therapies.\n"
                     "3. Helium is an essential component for cryogenics, as it remains a liquid at extremely low temperatures.\n"
                     "4. Xenon is utilized in space propulsion systems due to its high atomic weight and inertness."
    }

   
    scroll_offset = 0
    scroll_speed = 10
    padding = 20  
    wrapped_lines = []
    for section, text in content.items():
        wrapped_lines.append(f"{section}:")
        wrapped_lines.extend(textwrap.wrap(text, width=70))
        wrapped_lines.append("")  
    line_height = content_font.size("A")[1]
    content_width = max(content_font.size(line)[0] for line in wrapped_lines) + 2 * padding
    content_height = len(wrapped_lines) * line_height + 2 * padding

    box_width = min(content_width, WIDTH - 100)
    box_height = min(content_height, HEIGHT - 100)
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2
    button_width, button_height = 50, 30
    button_x, button_y = WIDTH - button_width - 10, 10
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    running = True
    while running:
        screen.blit(background, (0, 0))

        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(screen, SKY_BLUE, box_rect)
        pygame.draw.rect(screen, BLACK, box_rect, 2)

        pygame.draw.rect(screen, RED, button_rect)
        text_surface = button_font.render("X", True, WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_DOWN:
                    scroll_offset = min(scroll_offset + scroll_speed, max(0, content_height - box_height + padding))
                elif event.key == pygame.K_UP:
                    scroll_offset = max(scroll_offset - scroll_speed, 0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False

        
        y = box_y + padding - scroll_offset
        for line in wrapped_lines:
            if y + line_height > box_y + padding and y < box_y + box_height - padding:
                text_surface = content_font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, y + line_height // 2))
                screen.blit(text_surface, text_rect)
            y += line_height

        
        pygame.display.flip()

def noble_gas_trivia_adventure():
   
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Noble Gas Trivia Adventure")

    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (173, 216, 230)
    EXIT_BUTTON_COLOR = (255, 69, 0)

   
    font = pygame.font.Font("E:\\python\\map\\Berthany.otf", 40)

    
    background = pygame.image.load("E:\\python\\map\\noble gas.webp") 
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Load sounds
    correct_sound = pygame.mixer.Sound("E:\\python\\correct_sound.wav.wav")
    wrong_sound = pygame.mixer.Sound("E:\\python\\wronganswer-37702.mp3")
    end_game_sound = pygame.mixer.Sound("E:\\python\\goodresult-82807.mp3")

    # Trivia Questions
    questions = [
        {"question": "Which noble gas is used in advertising signs?", "options": ["Helium", "Neon", "Argon", "Krypton"], "answer": "Neon"},
        {"question": "Which noble gas is the lightest?", "options": ["Helium", "Neon", "Argon", "Xenon"], "answer": "Helium"},
        {"question": "Which noble gas is used in weather balloons?", "options": ["Krypton", "Helium", "Neon", "Argon"], "answer": "Helium"},
        {"question": "Which noble gas is most commonly used in light bulbs?", "options": ["Argon", "Neon", "Krypton", "Xenon"], "answer": "Argon"},
        {"question": "Which noble gas has the highest atomic number?", "options": ["Radon", "Xenon", "Krypton", "Argon"], "answer": "Radon"},
        {"question": "Which noble gas is used in car headlamps?", "options": ["Xenon", "Neon", "Argon", "Radon"], "answer": "Xenon"},
        {"question": "Which noble gas is radioactive?", "options": ["Radon", "Krypton", "Neon", "Argon"], "answer": "Radon"},
        {"question": "Which noble gas is used in plasma TVs?", "options": ["Neon", "Argon", "Xenon", "Helium"], "answer": "Xenon"},
        {"question": "Which noble gas is commonly used in welding?", "options": ["Argon", "Helium", "Krypton", "Neon"], "answer": "Argon"},
        {"question": "Which noble gas is used in cryogenics?", "options": ["Helium", "Neon", "Radon", "Argon"], "answer": "Helium"}
    ]

   
    current_question_index = 0
    score = 0
    showing_feedback = False
    feedback_timer = 0
    selected_option = None

   
    exit_button_rect = pygame.Rect(WIDTH - 50, 10, 40, 40)

    
    def draw_text_box(text, x, y, width, height, text_color, box_color, border_color=None, border_width=0):
        box_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, box_color, box_rect)
        if border_color and border_width > 0:
            pygame.draw.rect(screen, border_color, box_rect, border_width)

        lines = text.split('\n')
        line_height = font.get_linesize()
        total_text_height = line_height * len(lines)
        start_y = y + (height - total_text_height) // 2

        for i, line in enumerate(lines):
            rendered_text = font.render(line, True, text_color)
            text_rect = rendered_text.get_rect(center=(x + width // 2, start_y + i * line_height + line_height // 2))
            screen.blit(rendered_text, text_rect)

    
    def start_screen():
        while True:
            screen.fill(WHITE)
            screen.blit(background, (0, 0))

            draw_text_box(
                "Welcome to Noble Gas Trivia Adventure!\n\n"
                "Rules:\n"
                "1. Answer questions about noble gases.\n"
                "2. Correct answers give +10 points.\n"
                "3. Wrong answers subtract 5 points.\n"
                "4. Have fun and learn!",
                WIDTH // 2 - 400, HEIGHT // 2 - 200, 800, 300, WHITE, BLUE, BLACK, 2
            )

            start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50)
            pygame.draw.rect(screen, GREEN, start_button_rect)
            pygame.draw.rect(screen, WHITE, start_button_rect, 2)
            draw_text_box("Start", start_button_rect.x, start_button_rect.y, start_button_rect.width, 50, WHITE, GREEN)

            pygame.draw.rect(screen, EXIT_BUTTON_COLOR, exit_button_rect)
            pygame.draw.rect(screen, BLACK, exit_button_rect, 2)
            draw_text_box("X", exit_button_rect.x, exit_button_rect.y, 40, 40, WHITE, EXIT_BUTTON_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button_rect.collidepoint(event.pos):
                        return "start"
                    elif exit_button_rect.collidepoint(event.pos):
                        return "exit"

            pygame.display.flip()

   
    result = start_screen()
    if result == "exit":
        return 
    running = True
    while running:
        screen.blit(background, (0, 0))
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos):
                    return

                if not showing_feedback and "feedback_rects" in locals():
                    for i, rect in enumerate(feedback_rects):
                        if rect.collidepoint(event.pos):
                            selected_option = i
                            correct_option = questions[current_question_index]["options"].index(questions[current_question_index]["answer"])
                            if selected_option == correct_option:
                                score += 10
                                correct_sound.play()
                            else:
                                score -= 5
                                wrong_sound.play()
                            showing_feedback = True
                            feedback_timer = current_time + 2000

        if current_question_index < len(questions):
            current_question = questions[current_question_index]
            draw_text_box(
                current_question["question"],
                WIDTH // 2 - 400, HEIGHT // 2 - 200, 800, 100, WHITE, BLUE, BLACK, 2
            )

            feedback_rects = []
            correct_option = current_question["options"].index(current_question["answer"])
            for i, option in enumerate(current_question["options"]):
                option_rect = pygame.Rect(WIDTH // 2 - 400, HEIGHT // 2 - 50 + i * 70, 800, 50)
                if showing_feedback:
                    if i == selected_option and i != correct_option:
                        color = RED
                    elif i == correct_option:
                        color = GREEN
                    else:
                        color = BLUE
                else:
                    color = BLUE
                pygame.draw.rect(screen, color, option_rect)
                pygame.draw.rect(screen, BLACK, option_rect, 2)
                draw_text_box(option, option_rect.x, option_rect.y, option_rect.width, 50, WHITE, color)
                feedback_rects.append(option_rect)

            if showing_feedback and current_time > feedback_timer:
                showing_feedback = False
                selected_option = None
                current_question_index += 1
        else:
            draw_text_box(
                f"Game Over!\n\nYour Score: {score}/{len(questions) * 10}",
                WIDTH // 2 - 400, HEIGHT // 2 - 200, 800, 200, WHITE, GREEN if score > 0 else RED, BLACK, 2
            )
            end_game_sound.play()

        draw_text_box(f"Score: {score}", 10, 10, 200, 50, BLACK, WHITE)
        pygame.draw.rect(screen, EXIT_BUTTON_COLOR, exit_button_rect)
        pygame.draw.rect(screen, BLACK, exit_button_rect, 2)
        draw_text_box("X", exit_button_rect.x, exit_button_rect.y, 40, 40, WHITE, EXIT_BUTTON_COLOR)

        pygame.display.flip()

    pygame.quit()
def run_element_catcher_game():
    
    pygame.init()

    
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_width(), screen.get_height()
    pygame.display.set_caption("Element Catcher")

    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    DARK_GRAY = (50, 50, 50)
    DARK_RED = (139, 0, 0)
    LIGHT_GREEN = (0, 200, 0)
    DARK_YELLOW = (255, 165, 0)
    DARK_BROWN = (139, 69, 19)
    MENU_TEXT_COLOR = WHITE
    NEXT_TEXT_COLOR = LIGHT_GREEN

    
    clock = pygame.time.Clock()
    FPS = 60


    background = pygame.image.load(r"E:\\python\\background.png.webp")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    menu_page = pygame.image.load(r"E:\\python\\menupage.jpg")
    menu_page = pygame.transform.scale(menu_page, (WIDTH, HEIGHT))


    title_font = pygame.font.Font(r"E:\\python\\map\\Berthany.otf", 72)
    font = pygame.font.Font(r"E:\\python\\map\\Berthany.otf", 40)

    
    cauldron_image = pygame.image.load(r"E:\\python\\calldron-removebg-preview.png")
    cauldron_image = pygame.transform.scale(cauldron_image, (80, 80))
    cauldron_width, cauldron_height = cauldron_image.get_width(), cauldron_image.get_height()

    heart_image = pygame.image.load(r"E:\\python\\heart-removebg-preview.png")
    heart_image = pygame.transform.scale(heart_image, (30, 30))

   
    correct_sound = pygame.mixer.Sound(r"E:\\python\\correct_sound.wav.wav")
    wrong_sound = pygame.mixer.Sound(r"E:\\python\\wronganswer-37702.mp3")
    game_over_sound = pygame.mixer.Sound(r"E:\\python\\game-over-39-199830.mp3")
    bonus_sound = pygame.mixer.Sound(r"E:\\python\\game-bonus-144751.mp3")

    
    wizard_x = WIDTH // 2 - cauldron_width // 2
    wizard_y = HEIGHT - 120
    wizard_speed = 10

    element_width, element_height = 40, 40
    elements = []
    fall_speed = 5

    score = 0
    lives = 3
    periodic_table = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"]
    current_index = 0
    consecutive_correct = 0
    bonus_threshold = 5
    bonus_points = 50

   
    def draw_wizard(x, y):
        screen.blit(cauldron_image, (x, y))

    def draw_element(x, y, symbol, color):
        pygame.draw.rect(screen, color, (x, y, element_width, element_height))
        text = font.render(symbol, True, WHITE)
        text_rect = text.get_rect(center=(x + element_width // 2, y + element_height // 2))
        screen.blit(text, text_rect)

    def display_text(text, x, y, color=WHITE, custom_font=font):
        rendered_text = custom_font.render(text, True, color)
        screen.blit(rendered_text, (x, y))

    def draw_hearts(lives):
        for i in range(lives):
            screen.blit(heart_image, (10 + i * 35, 50))

    def generate_element():
        if random.random() < 0.3:
            symbol = periodic_table[current_index]
            color = LIGHT_GREEN 
        else:
            symbol = random.choice([x for x in periodic_table if x != periodic_table[current_index]])
            color = DARK_RED
        x = random.randint(0, WIDTH - element_width)
        y = -element_height
        return [x, y, symbol, color]

    def mode_selection():
        screen.fill(DARK_GRAY)
        screen.blit(menu_page, (0, 0))

        display_text("Catch Your Elements", WIDTH // 2 - title_font.size("Catch Your Elements")[0] // 2, HEIGHT // 2 - 200, DARK_YELLOW, title_font)

        box_width = 400
        box_height = 200
        box_x = WIDTH // 2 - box_width // 2
        box_y = HEIGHT // 2 - 100
        pygame.draw.rect(screen, DARK_BROWN, (box_x, box_y, box_width, box_height), border_radius=15)
        pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height), 3, border_radius=15)

        display_text("Choose a mode:", box_x + 20, box_y + 20, WHITE)
        display_text("1. Easy (9 Lives)", box_x + 20, box_y + 60, WHITE)
        display_text("2. Medium (6 Lives)", box_x + 20, box_y + 100, WHITE)
        display_text("3. Hard (3 Lives)", box_x + 20, box_y + 140, WHITE)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return 9
                    elif event.key == pygame.K_2:
                        return 6
                    elif event.key == pygame.K_3:
                        return 3

    def game_over_screen(score):
        screen.fill(DARK_GRAY)
        screen.blit(menu_page, (0, 0))

        box_width = 400
        box_height = 200
        box_x = WIDTH // 2 - box_width // 2
        box_y = HEIGHT // 2 - 100

        pygame.draw.rect(screen, DARK_BROWN, (box_x, box_y, box_width, box_height), border_radius=15)
        pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height), 3, border_radius=15)

        display_text("Game Over!", box_x + box_width // 2 - title_font.size("Game Over!")[0] // 2, box_y + 20, DARK_YELLOW, title_font)
        display_text(f"Score: {score}", box_x + 20, box_y + 100, WHITE)
        display_text("Press 'R' to Replay", box_x + 20, box_y + 150, WHITE)

        exit_button_rect = pygame.Rect(WIDTH - 60, 10, 40, 40)
        pygame.draw.rect(screen, DARK_RED, exit_button_rect)

        exit_font = pygame.font.Font(r"E:\\python\\map\\Berthany.otf", 40)
        exit_text = exit_font.render("X", True, WHITE)
        exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)
        screen.blit(exit_text, exit_text_rect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_button_rect.collidepoint(event.pos):
                        return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        elements.clear()
                        run_element_catcher_game()

    def draw_next_element():
        display_text("Next:", WIDTH - 150, 10, NEXT_TEXT_COLOR)
        display_text(periodic_table[current_index], WIDTH - 80, 10, NEXT_TEXT_COLOR)

    def main_game():
        nonlocal wizard_x, current_index, score, lives, consecutive_correct
        lives = mode_selection()
        elements.clear()
        score = 0
        current_index = 0
        consecutive_correct = 0

        running = True
        while running:
            screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and wizard_x > 0:
                wizard_x -= wizard_speed
            if keys[pygame.K_RIGHT] and wizard_x < WIDTH - cauldron_width:
                wizard_x += wizard_speed

            if random.randint(1, 30) == 1:
                elements.append(generate_element())

            for element in elements[:]:
                element[1] += fall_speed
                if wizard_x < element[0] < wizard_x + cauldron_width and wizard_y < element[1] + element_height < wizard_y + cauldron_height:
                    if element[2] == periodic_table[current_index]:
                        score += 10
                        consecutive_correct += 1
                        current_index = (current_index + 1) % len(periodic_table)
                        pygame.mixer.Sound.play(correct_sound)
                    else:
                        lives -= 1
                        pygame.mixer.Sound.play(wrong_sound)
                    elements.remove(element)
                elif element[1] > HEIGHT:
                    elements.remove(element)

            draw_wizard(wizard_x, wizard_y)
            for element in elements:
                draw_element(*element)

            display_text(f"Score: {score}", 10, 10, WHITE)
            draw_hearts(lives)
            draw_next_element()

            if lives <= 0:
                pygame.mixer.Sound.play(game_over_sound)
                game_over_screen(score)
                running = False

            pygame.display.flip()
            clock.tick(FPS)

    main_game()
def noble_gases_sorting_game():
    pygame.init()

   
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Sorting Mini-Game: Noble Gases")


    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (100, 149, 237)
    GREEN = (34, 139, 34)
    RED = (220, 20, 60)
    BABY_BLUE = (137, 207, 240)

   
    instruction_font = pygame.font.Font("E:\\python\\Berthany.otf", 40)
    element_font = pygame.font.Font("E:\\python\\Berthany.otf", 36)

    background = pygame.image.load("E:\\python\\map\\noble gas.webp")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    
    correct_sound = pygame.mixer.Sound("E:\\python\\map\\alkaline\\dnm\\correct_sound.wav.wav")

   
    properties = [
        {
            "name": "Atomic Number",
            "order": ["He", "Ne", "Ar", "Kr", "Xe", "Rn"],
            "instruction": "Arrange the noble gases in order of increasing atomic number.",
            "explanation": "The atomic number increases from helium (2) to radon (86)."
        },
        {
            "name": "Boiling Point",
            "order": ["He", "Ne", "Ar", "Kr", "Xe", "Rn"],
            "instruction": "Arrange the noble gases in order of increasing boiling point.",
            "explanation": "Boiling points increase with molecular weight and size of the atom."
        }
    ]

    
    current_property_index = 0
    current_property = properties[current_property_index]
    elements = [
        {"name": gas, "rect": pygame.Rect(WIDTH // 2 - 300 + i * 120, HEIGHT // 2 - 25, 100, 50), "dragging": False, "placed": False, "correct": False, "speed": [random.choice([-1, 1]), random.choice([-1, 1])]} 
        for i, gas in enumerate(current_property["order"])
    ]
    targets = [
        pygame.Rect(WIDTH // 2 - 300 + i * 120, HEIGHT // 2 + 100, 100, 50)
        for i in range(len(elements))
    ]

    def draw_background():
        """Draw the game background."""
        screen.blit(background, (0, 0))

    def draw_elements():
        """Draw draggable elements."""
        for element in elements:
            color = GREEN if element["correct"] else (RED if element["placed"] else BABY_BLUE)
            pygame.draw.rect(screen, color, element["rect"])
            text = element_font.render(element["name"], True, WHITE)
            text_rect = text.get_rect(center=element["rect"].center)
            screen.blit(text, text_rect)

    def draw_targets():
        """Draw target areas."""
        for i, target in enumerate(targets):
            pygame.draw.rect(screen, RED, target, 2)

    def draw_instructions_and_explanation():
        """Draw instructions and explanations for the current property."""
        instruction_lines = textwrap.wrap(current_property["instruction"], width=60)
        explanation_lines = textwrap.wrap(current_property["explanation"], width=60)

        for i, line in enumerate(instruction_lines):
            instruction_text = instruction_font.render(line, True, WHITE)
            instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, 50 + i * 40))
            screen.blit(instruction_text, instruction_rect)

        for i, line in enumerate(explanation_lines):
            explanation_text = instruction_font.render(line, True, WHITE)
            explanation_rect = explanation_text.get_rect(center=(WIDTH // 2, HEIGHT - 150 + i * 40))
            screen.blit(explanation_text, explanation_rect)

    def move_elements():
        """Move elements around the screen."""
        for element in elements:
            if not element["dragging"] and not element["placed"]:
                element["rect"].x += element["speed"][0]
                element["rect"].y += element["speed"][1]

                if element["rect"].left < 0 or element["rect"].right > WIDTH:
                    element["speed"][0] *= -1
                if element["rect"].top < 0 or element["rect"].bottom > HEIGHT:
                    element["speed"][1] *= -1

    def check_completion():
        """Check if the elements are sorted correctly."""
        for i, element in enumerate(elements):
            if not targets[i].collidepoint(element["rect"].center) or not element["correct"]:
                return False
        return True

    
    running = True
    while running:
        screen.fill(WHITE)
        draw_background()
        move_elements()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for element in elements:
                    if element["rect"].collidepoint(event.pos) and not element["placed"]:
                        element["dragging"] = True

            elif event.type == pygame.MOUSEBUTTONUP:
                for i, element in enumerate(elements):
                    if element["dragging"]:
                        element["dragging"] = False
                        if targets[i].collidepoint(element["rect"].center):
                            if element["name"] == current_property["order"][i]:
                                element["rect"].center = targets[i].center
                                element["placed"] = True
                                element["correct"] = True
                                correct_sound.play() 
                            else:
                                element["placed"] = True
                                element["correct"] = False

            elif event.type == pygame.MOUSEMOTION:
                for element in elements:
                    if element["dragging"]:
                        element["rect"].x += event.rel[0]
                        element["rect"].y += event.rel[1]

      
        draw_elements()
        draw_targets()
        draw_instructions_and_explanation()

        
        if check_completion():
            current_property_index += 1
            if current_property_index >= len(properties):
                print("Game completed!")
                running = False
            else:
                current_property = properties[current_property_index]
                elements = [
                    {"name": gas, "rect": pygame.Rect(WIDTH // 2 - 300 + i * 120, HEIGHT // 2 - 25, 100, 50), "dragging": False, "placed": False, "correct": False, "speed": [random.choice([-1, 1]), random.choice([-1, 1])]} 
                    for i, gas in enumerate(current_property["order"])
                ]

        
        pygame.display.flip()

def transition_metals_info():
    
    pygame.init()

    
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Transition Metals Info")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    ORANGE = (205, 127, 50)
    RED = (255, 0, 0)

    
    content_font = pygame.font.Font("E:\\python\\Berthany.otf", 36)
    button_font = pygame.font.Font(None, 36)


    background = pygame.image.load("E:\\python\\map\\metal.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    
    content = {
        "Introduction": "Transition metals are elements in groups 3-12 of the periodic table. "
                        "They are known for their high melting points, malleability, and ability to form colorful compounds.",
        "Details": "1. Found in the d-block of the periodic table.\n"
                   "2. Includes iron, copper, silver, gold, tungsten, and more.\n"
                   "3. Known for their ability to form multiple oxidation states.\n"
                   "4. Many are excellent conductors of heat and electricity.",
        "Important Information": "1. Mercury is the only transition metal that is liquid at room temperature.\n"
                                "2. Tungsten has the highest melting point of all elements and is used in light bulb filaments.\n"
                                "3. Iron is essential for the human body as it forms the core of hemoglobin.\n"
                                "4. Platinum is highly resistant to corrosion and is used in catalytic converters.\n"
                                "5. Chromium adds durability to stainless steel, making it rust-resistant.",
        "Usage and Applications": "1. Copper is widely used in electrical wiring due to its excellent conductivity.\n"
                                "2. Zinc is used to coat galvanized steel, protecting it from rust.\n"
                                "3. Cobalt is a key component in rechargeable batteries.\n"
                                "4. Gold and platinum are used in jewelry and as a store of value.\n"
                                "5. Iridium and rhodium are known for their exceptional resistance to corrosion.",
        "Storage and Safety": "1. Most transition metals are stable under normal conditions and do not require special storage.\n"
                              "2. Reactive metals like iron should be protected from moisture to prevent rusting.\n"
                              "3. Mercury must be stored in sealed containers to prevent toxic vapor release.",
        "Fun Facts": "1. Transition metals form colorful compounds, such as copper sulfate's bright blue and potassium dichromate's orange.\n"
                     "2. Platinum is 30 times rarer than gold.\n"
                     "3. Tungsten’s melting point is an incredible 3,422°C.\n"
                     "4. The Statue of Liberty's green color is due to the oxidation of its copper surface.\n"
                     "5. Chromium gives emeralds their brilliant green color."
    }

    
    scroll_offset = 0
    scroll_speed = 10
    padding = 20  
   
    wrapped_lines = []
    for section, text in content.items():
        wrapped_lines.append(f"{section}:")
        wrapped_lines.extend(textwrap.wrap(text, width=70))
        wrapped_lines.append("") 

    
    line_height = content_font.size("A")[1]
    content_width = max(content_font.size(line)[0] for line in wrapped_lines) + 2 * padding
    content_height = len(wrapped_lines) * line_height + 2 * padding

    
    box_width = min(content_width, WIDTH - 100)
    box_height = min(content_height, HEIGHT - 100)
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2

   
    button_width, button_height = 50, 30
    button_x, button_y = WIDTH - button_width - 10, 10
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    
    running = True
    while running:
        screen.blit(background, (0, 0))

        
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(screen, ORANGE, box_rect)
        pygame.draw.rect(screen, BLACK, box_rect, 2)

      
        pygame.draw.rect(screen, RED, button_rect)
        text_surface = button_font.render("X", True, WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_DOWN:
                    scroll_offset = min(scroll_offset + scroll_speed, max(0, content_height - box_height + padding))
                elif event.key == pygame.K_UP:
                    scroll_offset = max(scroll_offset - scroll_speed, 0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False

        
        y = box_y + padding - scroll_offset
        for line in wrapped_lines:
            if y + line_height > box_y + padding and y < box_y + box_height - padding:
                text_surface = content_font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, y + line_height // 2))
                screen.blit(text_surface, text_rect)
            y += line_height

        
        pygame.display.flip()

def transition_metals_trivia_adventure():
    pygame.init()

    
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Transition Metals Trivia Adventure")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (144, 12, 63)
    EXIT_BUTTON_COLOR = (255, 69, 0)

   
    font = pygame.font.Font("E:\\python\\map\\Berthany.otf", 40)

    
    background = pygame.image.load("E:\\python\\map\\metal.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    
    correct_sound = pygame.mixer.Sound("E:\\python\\correct_sound.wav.wav")
    wrong_sound = pygame.mixer.Sound("E:\\python\\wronganswer-37702.mp3")
    end_game_sound = pygame.mixer.Sound("E:\\python\\goodresult-82807.mp3")

    
    questions = [
        {"question": "Which transition metal is liquid at room temperature?", "options": ["Iron", "Mercury", "Nickel", "Cobalt"], "answer": "Mercury"},
        {"question": "Which metal is known for its use in light bulb filaments?", "options": ["Tungsten", "Copper", "Zinc", "Chromium"], "answer": "Tungsten"},
        {"question": "Which transition metal is essential in hemoglobin?", "options": ["Iron", "Copper", "Zinc", "Manganese"], "answer": "Iron"},
        {"question": "Which metal is commonly used as a catalyst in catalytic converters?", "options": ["Platinum", "Gold", "Silver", "Aluminum"], "answer": "Platinum"},
        {"question": "Which transition metal is used in stainless steel?", "options": ["Nickel", "Chromium", "Titanium", "Vanadium"], "answer": "Chromium"},
        {"question": "Which metal has the highest melting point of all elements?", "options": ["Tungsten", "Iron", "Platinum", "Titanium"], "answer": "Tungsten"},
        {"question": "Which metal is known for its use in rechargeable batteries?", "options": ["Nickel", "Cobalt", "Zinc", "Copper"], "answer": "Cobalt"},
        {"question": "Which transition metal is most resistant to corrosion?", "options": ["Gold", "Platinum", "Iridium", "Rhodium"], "answer": "Platinum"},
        {"question": "Which metal is used to coat galvanized steel?", "options": ["Zinc", "Nickel", "Copper", "Iron"], "answer": "Zinc"},
        {"question": "Which metal is commonly used in electrical wiring?", "options": ["Copper", "Silver", "Gold", "Nickel"], "answer": "Copper"}
    ]

    
    current_question_index = 0
    score = 0
    showing_feedback = False
    feedback_timer = 0
    selected_option = None


    exit_button_rect = pygame.Rect(WIDTH - 50, 10, 40, 40)

    def draw_text_box(text, x, y, width, height, text_color, box_color, border_color=None, border_width=0):
        box_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, box_color, box_rect)
        if border_color and border_width > 0:
            pygame.draw.rect(screen, border_color, box_rect, border_width)

        lines = text.split('\n')
        line_height = font.get_linesize()
        total_text_height = line_height * len(lines)
        start_y = y + (height - total_text_height) // 2

        for i, line in enumerate(lines):
            rendered_text = font.render(line, True, text_color)
            text_rect = rendered_text.get_rect(center=(x + width // 2, start_y + i * line_height + line_height // 2))
            screen.blit(rendered_text, text_rect)

    
    def start_screen():
        while True:
            screen.fill(WHITE)
            screen.blit(background, (0, 0))

            draw_text_box(
                "Welcome to Transition Metals Trivia Adventure!\n\n"
                "Rules:\n"
                "1. Answer questions about transition metals.\n"
                "2. Correct answers give +10 points.\n"
                "3. Wrong answers subtract 5 points.\n"
                "4. Have fun and learn!",
                WIDTH // 2 - 400, HEIGHT // 2 - 200, 800, 300, WHITE, BLUE, BLACK, 2
            )

            start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50)
            pygame.draw.rect(screen, GREEN, start_button_rect)
            pygame.draw.rect(screen, WHITE, start_button_rect, 2)
            draw_text_box("Start", start_button_rect.x, start_button_rect.y, start_button_rect.width, 50, WHITE, GREEN)

            pygame.draw.rect(screen, EXIT_BUTTON_COLOR, exit_button_rect)
            pygame.draw.rect(screen, BLACK, exit_button_rect, 2)
            draw_text_box("X", exit_button_rect.x, exit_button_rect.y, 40, 40, WHITE, EXIT_BUTTON_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button_rect.collidepoint(event.pos):
                        return "start"
                    elif exit_button_rect.collidepoint(event.pos):
                        return "exit"

            pygame.display.flip()

   
    result = start_screen()
    if result == "exit":
        return 

    running = True
    while running:
        screen.blit(background, (0, 0))
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos):
                    return

                if not showing_feedback and "feedback_rects" in locals():
                    for i, rect in enumerate(feedback_rects):
                        if rect.collidepoint(event.pos):
                            selected_option = i
                            correct_option = questions[current_question_index]["options"].index(questions[current_question_index]["answer"])
                            if selected_option == correct_option:
                                score += 10
                                correct_sound.play()
                            else:
                                score -= 5
                                wrong_sound.play()
                            showing_feedback = True
                            feedback_timer = current_time + 2000

        if current_question_index < len(questions):
            current_question = questions[current_question_index]
            draw_text_box(
                current_question["question"],
                WIDTH // 2 - 400, HEIGHT // 2 - 200, 800, 100, WHITE, BLUE, BLACK, 2
            )

            feedback_rects = []
            correct_option = current_question["options"].index(current_question["answer"])
            for i, option in enumerate(current_question["options"]):
                option_rect = pygame.Rect(WIDTH // 2 - 400, HEIGHT // 2 - 50 + i * 70, 800, 50)
                if showing_feedback:
                    if i == selected_option and i != correct_option:
                        color = RED
                    elif i == correct_option:
                        color = GREEN
                    else:
                        color = BLUE
                else:
                    color = BLUE
                pygame.draw.rect(screen, color, option_rect)
                pygame.draw.rect(screen, BLACK, option_rect, 2)
                draw_text_box(option, option_rect.x, option_rect.y, option_rect.width, 50, WHITE, color)
                feedback_rects.append(option_rect)

            if showing_feedback and current_time > feedback_timer:
                showing_feedback = False
                selected_option = None
                current_question_index += 1
        else:
            draw_text_box(
                f"Game Over!\n\nYour Score: {score}/{len(questions) * 10}",
                WIDTH // 2 - 400, HEIGHT // 2 - 200, 800, 200, WHITE, GREEN if score > 0 else RED, BLACK, 2
            )
            end_game_sound.play()

        draw_text_box(f"Score: {score}", 10, 10, 200, 50, BLACK, WHITE)
        pygame.draw.rect(screen, EXIT_BUTTON_COLOR, exit_button_rect)
        pygame.draw.rect(screen, BLACK, exit_button_rect, 2)
        draw_text_box("X", exit_button_rect.x, exit_button_rect.y, 40, 40, WHITE, EXIT_BUTTON_COLOR)

        pygame.display.flip()

    pygame.quit()

def run_halogen_info():
    
    pygame.init()

   
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Halogens Info")


    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 163, 108)
    RED = (255, 0, 0)

  
    content_font = pygame.font.Font("E:\\python\\Berthany.otf", 36)
    button_font = pygame.font.Font("E:\\python\\Berthany.otf", 36)


    background = pygame.image.load("E:\\python\\map\\halogen.webp")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    
    content = {
        "Introduction": "Halogens are a group of nonmetals in Group 17 of the periodic table. They are highly reactive and have a wide range of applications in industry and daily life.",
        "Details": "1. Includes fluorine, chlorine, bromine, iodine, and astatine.\n"
                   "2. Known for their high electronegativity and reactivity.\n"
                   "3. Exist in all three states of matter at room temperature (e.g., fluorine is a gas, bromine is a liquid, iodine is a solid).",
        "Important Information": "1. Chlorine is used to disinfect water and in the production of PVC.\n"
                                  "2. Fluorine is used in toothpaste to prevent cavities.\n"
                                  "3. Bromine is used in fire retardants and certain dyes.\n"
                                  "4. Iodine is essential for thyroid function and is used as a disinfectant.\n"
                                  "5. Astatine is a rare and radioactive element with limited applications.",
        "Usage and Applications": "1. Halogens are used in making disinfectants, bleach, and water purification chemicals.\n"
                                   "2. Fluorine compounds are used in non-stick cookware and refrigeration.\n"
                                   "3. Bromine compounds are key in flame retardants.\n"
                                   "4. Iodine is used in medical antiseptics and in iodized salt to prevent deficiencies.",
        "Storage and Safety": "1. Halogens must be stored carefully due to their high reactivity and potential toxicity.\n"
                              "2. Fluorine and chlorine should be stored in specialized containers under controlled conditions.\n"
                              "3. Bromine requires sealed glass or plastic containers to avoid vapor release.\n"
                              "4. Iodine should be kept in a dark, cool place to prevent sublimation.",
        "Fun Facts": "1. Fluorine is the most reactive and electronegative element.\n"
                     "2. Chlorine gas was used in World War I as a chemical weapon.\n"
                     "3. Bromine is the only nonmetal that is liquid at room temperature.\n"
                     "4. Iodine turns purple when heated.\n"
                     "5. Astatine is so rare that less than 1 gram exists on Earth naturally."
    }

    
    scroll_offset = 0
    scroll_speed = 10
    padding = 20 

    
    wrapped_lines = []
    for section, text in content.items():
        wrapped_lines.append(f"{section}:")
        wrapped_lines.extend(textwrap.wrap(text, width=70))
        wrapped_lines.append("")  

    
    line_height = content_font.size("A")[1]
    content_width = max(content_font.size(line)[0] for line in wrapped_lines) + 2 * padding
    content_height = len(wrapped_lines) * line_height + 2 * padding

    
    box_width = min(content_width, WIDTH - 100)
    box_height = min(content_height, HEIGHT - 100)
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2

    button_width, button_height = 50, 30
    button_x, button_y = WIDTH - button_width - 10, 10
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    
    running = True
    while running:
        screen.blit(background, (0, 0))

       
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(screen, GREEN, box_rect)
        pygame.draw.rect(screen, BLACK, box_rect, 2)

        pygame.draw.rect(screen, RED, button_rect)
        text_surface = button_font.render("X", True, WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_DOWN:
                    scroll_offset = min(scroll_offset + scroll_speed, max(0, content_height - box_height + padding))
                elif event.key == pygame.K_UP:
                    scroll_offset = max(scroll_offset - scroll_speed, 0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False

        
        y = box_y + padding - scroll_offset
        for line in wrapped_lines:
            if y + line_height > box_y + padding and y < box_y + box_height - padding:
                text_surface = content_font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, y + line_height // 2))
                screen.blit(text_surface, text_rect)
            y += line_height

        
        pygame.display.flip()

def halogen_trivia_adventure():
    
    pygame.init()

    
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Halogen Trivia Adventure")

   
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    PURPLE = (88, 24, 69)
    EXIT_BUTTON_COLOR = (255, 69, 0)

    
    font = pygame.font.Font("E:\\python\\Berthany.otf", 40)

    
    background = pygame.image.load("E:\\python\\map\\halogen\\bg.webp")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    
    correct_sound = pygame.mixer.Sound("E:\\python\\correct_sound.wav.wav")
    wrong_sound = pygame.mixer.Sound("E:\\python\\wronganswer-37702.mp3")
    end_game_sound = pygame.mixer.Sound("E:\\python\\goodresult-82807.mp3")

    
    questions = [
        {"question": "Which halogen is the most reactive?", "options": ["Chlorine", "Fluorine", "Bromine", "Iodine"], "answer": "Fluorine"},
        {"question": "Which halogen is a liquid at room temperature?", "options": ["Chlorine", "Fluorine", "Bromine", "Iodine"], "answer": "Bromine"},
        {"question": "Which halogen is used in antiseptics?", "options": ["Chlorine", "Fluorine", "Bromine", "Iodine"], "answer": "Iodine"},
        {"question": "Which halogen is commonly used in toothpaste?", "options": ["Chlorine", "Fluorine", "Bromine", "Iodine"], "answer": "Fluorine"},
        {"question": "Which halogen is yellow-green in color?", "options": ["Chlorine", "Fluorine", "Bromine", "Iodine"], "answer": "Chlorine"},
        {"question": "Which halogen is the least reactive?", "options": ["Fluorine", "Chlorine", "Iodine", "Astatine"], "answer": "Astatine"},
        {"question": "Which halogen is used in water purification?", "options": ["Chlorine", "Fluorine", "Bromine", "Iodine"], "answer": "Chlorine"},
        {"question": "Which halogen is violet in its solid form?", "options": ["Chlorine", "Fluorine", "Bromine", "Iodine"], "answer": "Iodine"},
        {"question": "Which halogen is the heaviest?", "options": ["Fluorine", "Chlorine", "Bromine", "Astatine"], "answer": "Astatine"},
        {"question": "Which halogen forms a brownish-red liquid?", "options": ["Chlorine", "Fluorine", "Bromine", "Iodine"], "answer": "Bromine"},
    ]

    current_question_index = 0
    score = 0
    showing_feedback = False
    feedback_timer = 0
    selected_option = None

   
    exit_button_rect = pygame.Rect(WIDTH - 50, 10, 40, 40)

   
    def draw_text_box(text, x, y, width, height, text_color, box_color, border_color=None, border_width=0):
        box_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, box_color, box_rect)
        if border_color and border_width > 0:
            pygame.draw.rect(screen, border_color, box_rect, border_width)

        lines = text.split('\n')
        line_height = font.get_linesize()
        total_text_height = line_height * len(lines)
        start_y = y + (height - total_text_height) // 2

        for i, line in enumerate(lines):
            rendered_text = font.render(line, True, text_color)
            text_rect = rendered_text.get_rect(center=(x + width // 2, start_y + i * line_height + line_height // 2))
            screen.blit(rendered_text, text_rect)

    
    def start_screen():
        while True:
            screen.fill(WHITE)
            screen.blit(background, (0, 0))

            draw_text_box(
                "Welcome to Halogen Trivia Adventure!\n\n"
                "Rules:\n"
                "1. Answer questions about halogens.\n"
                "2. Correct answers give +10 points.\n"
                "3. Wrong answers subtract 5 points.\n"
                "4. Have fun and learn!",
                WIDTH // 2 - 400, HEIGHT // 2 - 200, 800, 300, WHITE, PURPLE, BLACK, 2
            )

            start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50)
            pygame.draw.rect(screen, GREEN, start_button_rect)
            pygame.draw.rect(screen, WHITE, start_button_rect, 2)
            draw_text_box("Start", start_button_rect.x, start_button_rect.y, start_button_rect.width, 50, WHITE, GREEN)

            pygame.draw.rect(screen, EXIT_BUTTON_COLOR, exit_button_rect)
            pygame.draw.rect(screen, BLACK, exit_button_rect, 2)
            draw_text_box("X", exit_button_rect.x, exit_button_rect.y, 40, 40, WHITE, EXIT_BUTTON_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button_rect.collidepoint(event.pos):
                        return "start"
                    elif exit_button_rect.collidepoint(event.pos):
                        return "exit"

            pygame.display.flip()

    
    result = start_screen()
    if result == "exit":
        return  

    running = True
    while running:
        screen.blit(background, (0, 0))
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos):
                    return

                if not showing_feedback and "feedback_rects" in locals():
                    for i, rect in enumerate(feedback_rects):
                        if rect.collidepoint(event.pos):
                            selected_option = i
                            correct_option = questions[current_question_index]["options"].index(questions[current_question_index]["answer"])
                            if selected_option == correct_option:
                                score += 10
                                correct_sound.play()
                            else:
                                score -= 5
                                wrong_sound.play()
                            showing_feedback = True
                            feedback_timer = current_time + 2000

        if current_question_index < len(questions):
            current_question = questions[current_question_index]
            draw_text_box(
                current_question["question"],
                WIDTH // 2 - 400, HEIGHT // 2 - 200, 800, 100, WHITE, PURPLE, BLACK, 2
            )

            feedback_rects = []
            correct_option = current_question["options"].index(current_question["answer"])
            for i, option in enumerate(current_question["options"]):
                option_rect = pygame.Rect(WIDTH // 2 - 400, HEIGHT // 2 - 50 + i * 70, 800, 50)
                if showing_feedback:
                    if i == selected_option and i != correct_option:
                        color = RED
                    elif i == correct_option:
                        color = GREEN
                    else:
                        color = PURPLE
                else:
                    color = PURPLE
                pygame.draw.rect(screen, color, option_rect)
                pygame.draw.rect(screen, BLACK, option_rect, 2)
                draw_text_box(option, option_rect.x, option_rect.y, option_rect.width, 50, WHITE, color)
                feedback_rects.append(option_rect)

            if showing_feedback and current_time > feedback_timer:
                showing_feedback = False
                selected_option = None
                current_question_index += 1
        else:
            draw_text_box(
                f"Game Over!\n\nYour Score: {score}/{len(questions) * 10}",
                WIDTH // 2 - 400, HEIGHT // 2 - 200, 800, 200, WHITE, GREEN if score > 0 else RED, BLACK, 2
            )
            end_game_sound.play()

        draw_text_box(f"Score: {score}", 10, 10, 200, 50, BLACK, WHITE)
        pygame.draw.rect(screen, EXIT_BUTTON_COLOR, exit_button_rect)
        pygame.draw.rect(screen, BLACK, exit_button_rect, 2)
        draw_text_box("X", exit_button_rect.x, exit_button_rect.y, 40, 40, WHITE, EXIT_BUTTON_COLOR)

        pygame.display.flip()

    pygame.quit()
def run_halogen_defense():
    
    pygame.init()

    
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Halogen Defense")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREY = (200, 200, 200)
    EXIT_BUTTON_COLOR = (255, 69, 0)
    START_BUTTON_COLOR = (0, 255, 0)

    
    clock = pygame.time.Clock()

   
    font = pygame.font.Font("E:\\python\\Berthany.otf", 30)
    big_font = pygame.font.Font("E:\\python\\Berthany.otf", 60)
    reaction_font = pygame.font.Font("E:\\python\\Berthany.otf", 80)

    
    HALOGENS = ["F", "Cl", "Br", "I"]
    ALKALI_METALS = ["Na", "K", "Li"]

    
    reaction_sound = pygame.mixer.Sound("E:\\python\\map\\halogen\\ksound (1).wav")
    game_over_sound = pygame.mixer.Sound("E:\\python\\game-over-39-199830.mp3")


    bg_image = pygame.image.load("E:\\python\\map\\halogen\\bg.png")
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

    
    class Particle:
        def __init__(self, x, y, color, multiplier, lifetime):
            self.x = x
            self.y = y
            self.color = color
            self.multiplier = multiplier
            self.lifetime = lifetime
            self.time_alive = 0
            self.velocity = [random.uniform(-2, 2) * multiplier, random.uniform(-2, 2) * multiplier]

        def update(self):
            self.x += self.velocity[0]
            self.y += self.velocity[1]
            self.time_alive += 1
            self.velocity[1] += 0.1 

        def draw(self):
            if self.time_alive < self.lifetime:
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 3)

    class Enemy:
        def __init__(self, x, y, metal_type):
            self.x = x
            self.y = y
            self.type = metal_type
            self.health = 100
            self.speed = 1
            self.alive = True

        def move(self):
            if self.alive:
                self.x -= self.speed

        def draw(self):
            if self.alive:
                pygame.draw.circle(screen, RED, (self.x, self.y), 25)
                text = font.render(self.type, True, BLACK)
                screen.blit(text, (self.x - 15, self.y - 10))

    class Halogen:
        def __init__(self, x, y, halogen_type):
            self.initial_x = x
            self.initial_y = y
            self.x = x
            self.y = y
            self.type = halogen_type
            self.dragging = False

        def reset_position(self):
            self.x = self.initial_x
            self.y = self.initial_y

        def draw(self):
            pygame.draw.circle(screen, BLUE, (self.x, self.y), 30)
            text = font.render(self.type, True, WHITE)
            screen.blit(text, (self.x - 10, self.y - 10))

        def is_dragged(self, mouse_pos):
            return math.sqrt((mouse_pos[0] - self.x) ** 2 + (mouse_pos[1] - self.y) ** 2) < 30

    
    global reaction_message, cannon_halogen, score, killed_enemies, game_over, passed_enemies
    enemies = []
    halogens = [Halogen(50, HEIGHT - 200 - i * 80, h) for i, h in enumerate(HALOGENS)]
    reaction_message = ""
    score = 0
    killed_enemies = 0
    game_over = False
    particles = []
    passed_enemies = 0  

    
    fort_rect = pygame.Rect(100, HEIGHT // 2 - 100, 150, 200)
    cannon_center = (fort_rect.centerx, fort_rect.top)
    cannon_halogen = None

    
    exit_button_rect = pygame.Rect(WIDTH - 50, 10, 40, 40)
    start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 80)

    
    def show_rules():
        running = True
        while running:
            screen.fill(WHITE)
            screen.blit(bg_image, (0, 0))  
            rules_text = (
                "Welcome to Halogen Defense!\n\n"
                "Objective: Protect the Halogen Kingdom from alkali metals!\n\n"
                "How to Play:\n"
                "- Drag and drop a halogen (F, Cl, Br, I) into the cannon.\n"
                "- Target an alkali metal (Na, K, Li) to neutralize it.\n"
                "- The reaction will show the resulting compound.\n"
                "- Neutralize 15 enemies to win!\n\n"
                "Click Start to begin!"
            )
            y_offset = 100
            for line in rules_text.split("\n"):
                line_rendered = font.render(line, True, BLACK)
                line_rect = line_rendered.get_rect(center=(WIDTH // 2, y_offset))
                screen.blit(line_rendered, line_rect)
                y_offset += 40

            
            pygame.draw.rect(screen, EXIT_BUTTON_COLOR, exit_button_rect)
            pygame.draw.rect(screen, BLACK, exit_button_rect, 2)
            exit_text = font.render("X", True, WHITE)
            screen.blit(exit_text, (exit_button_rect.x + 10, exit_button_rect.y + 5))

            pygame.draw.rect(screen, START_BUTTON_COLOR, start_button_rect)
            start_text = big_font.render("START", True, WHITE)
            screen.blit(start_text, (start_button_rect.x + 50, start_button_rect.y + 20))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_button_rect.collidepoint(event.pos):
                        return "exit"
                    elif start_button_rect.collidepoint(event.pos):
                        print("Start button pressed")  # Debugging message
                        return "start"

            pygame.display.flip()

    
    def main_game():
        global reaction_message, cannon_halogen, score, killed_enemies, game_over, passed_enemies

        
        reaction_message = ""
        cannon_halogen = None
        score = 0
        killed_enemies = 0
        passed_enemies = 0
        game_over = False

        running = True
        selected_halogen = None
        spawn_timer = 0

        while running:
            screen.blit(bg_image, (0, 0)) 
            pygame.draw.rect(screen, GREY, fort_rect)
            pygame.draw.circle(screen, BLACK, cannon_center, 40)
            if cannon_halogen:
                pygame.draw.circle(screen, BLUE, cannon_center, 30)
                text = font.render(cannon_halogen.type, True, WHITE)
                screen.blit(text, (cannon_center[0] - 10, cannon_center[1] - 10))

            if not game_over:
                
                spawn_timer += 1
                if spawn_timer > 120:
                    spawn_timer = 0
                    metal_type = random.choice(ALKALI_METALS)
                    enemies.append(Enemy(WIDTH, random.randint(100, HEIGHT - 100), metal_type))

            
            for enemy in enemies[:]:
                enemy.move()
                enemy.draw()
                if enemy.x < 0:
                    enemies.remove(enemy)
                    passed_enemies += 1
                elif not enemy.alive:
                    enemies.remove(enemy)

            
            for halogen in halogens:
                halogen.draw()

           
            if reaction_message:
                reaction_text = reaction_font.render(reaction_message, True, WHITE)
                screen.blit(reaction_text, (WIDTH // 2 - reaction_text.get_width() // 2, 20))

            # Check win/lose conditions
            if killed_enemies >= 15 and not game_over:
                game_over = True
                reaction_message = "Congratulations! You have successfully neutralized all enemies!"
                pygame.mixer.music.load("E:\\python\\goodresult-82807.mp3")
                pygame.mixer.music.play()

            if passed_enemies >= 3:
                game_over = True
                reaction_message = "Game Over! Too many enemies crossed!"
                game_over_sound.play()

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for halogen in halogens:
                        if halogen.is_dragged(mouse_pos):
                            halogen.dragging = True
                            selected_halogen = halogen
                            break

                    if exit_button_rect.collidepoint(event.pos):
                        return "exit"

                elif event.type == pygame.MOUSEBUTTONUP:
                    if selected_halogen:
                        selected_halogen.dragging = False
                        if math.sqrt((selected_halogen.x - cannon_center[0]) ** 2 + (selected_halogen.y - cannon_center[1]) ** 2) < 40:
                            cannon_halogen = selected_halogen
                            selected_halogen.reset_position()
                            selected_halogen = None

                elif event.type == pygame.MOUSEMOTION and selected_halogen and selected_halogen.dragging:
                    selected_halogen.x, selected_halogen.y = event.pos

            # Handle cannon and shooting
            if cannon_halogen:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                pygame.draw.line(screen, BLUE, cannon_center, (mouse_x, mouse_y), 3)
                pygame.draw.circle(screen, BLUE, (mouse_x, mouse_y), 30, 2)

                if pygame.mouse.get_pressed()[0]: 
                    for enemy in enemies:
                        if (
                            enemy.alive
                            and math.sqrt((enemy.x - mouse_x) ** 2 + (enemy.y - mouse_y) ** 2) < 30
                        ):
                            reaction_message = f"{enemy.type} + {cannon_halogen.type} -> {enemy.type}{cannon_halogen.type}"
                            enemy.alive = False
                            score += 10
                            killed_enemies += 1
                            cannon_halogen = None
                            reaction_sound.play()
                            for _ in range(100):
                                particles.append(Particle(enemy.x, enemy.y, (255, 255, 0), 1, 160))
                            break

            
            for particle in particles[:]:
                particle.update()
                particle.draw()
                if particle.time_alive > particle.lifetime:
                    particles.remove(particle)

            
            pygame.draw.rect(screen, EXIT_BUTTON_COLOR, exit_button_rect)
            pygame.draw.rect(screen, BLACK, exit_button_rect, 2)
            exit_text = font.render("X", True, WHITE)
            screen.blit(exit_text, (exit_button_rect.x + 10, exit_button_rect.y + 5))

            pygame.display.flip()
            clock.tick(60)

            
            if game_over:
                if killed_enemies == 15:
                    show_victory_screen()
                else:
                    show_game_over_screen()
                running = False   

    def show_game_over_screen():
        screen.fill(WHITE)
        screen.blit(bg_image, (0, 0))  
        end_message = f"Game Over! Enemies Killed: {killed_enemies} Enemies Crossed: {passed_enemies}"
        end_text = big_font.render(end_message, True, BLACK)
        screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - end_text.get_height() // 2))
        
        pygame.display.flip()
        pygame.time.wait(5000) 

    def show_victory_screen():
        screen.fill(WHITE)
        screen.blit(bg_image, (0, 0))  
        victory_message = f"Victory! Enemies Killed: {killed_enemies}"
        victory_text = big_font.render(victory_message, True, BLACK)
        screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 2 - victory_text.get_height() // 2))
        
        pygame.display.flip()
        pygame.time.wait(5000)  
    # Main loop
    while True:
        result = show_rules()
        print(f"Result from show_rules: {result}") 
        if result == "exit":
            pygame.quit()
            sys.exit()
        elif result == "start":
            print("Starting main game...")  
            result = main_game()
            print(f"Result from main_game: {result}") 
            if result == "exit":
                pygame.quit()
                sys.exit()


def halogen_sorting_game():
   
    pygame.init()

  
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Halogens Sorting Mini-Game")

    WHITE = (255, 255, 255)
    BLACK = (88, 24, 69)
    BLUE = (100, 149, 237)
    GREEN = (34, 139, 34)
    RED = (220, 20, 60)
    BABY_BLUE = (137, 207, 240)

   
    instruction_font = pygame.font.Font("E:\\python\\Berthany.otf", 40)
    element_font = pygame.font.Font(None, 36)

    
    background = pygame.image.load("E:\\python\\map\\halogen\\bg.webp")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

   
    correct_sound = pygame.mixer.Sound("E:\\python\\correct_sound.wav.wav")

    
    properties = [
        {
            "name": "Reactivity with Metals",
            "order": ["F", "Cl", "Br", "I", "At"],
            "instruction": "Arrange the halogens in order of decreasing reactivity with metals, starting with the most reactive and ending with the least reactive.",
            "explanation": "Reactivity decreases down the group due to increasing atomic size and decreasing electronegativity."
        },
        {
            "name": "Electronegativity",
            "order": ["F", "Cl", "Br", "I", "At"],
            "instruction": "Arrange the halogens in order of decreasing electronegativity, starting with the highest and ending with the lowest.",
            "explanation": "Electronegativity decreases down the group as atomic size increases."
        },
        {
            "name": "Boiling Point",
            "order": ["At", "I", "Br", "Cl", "F"],
            "instruction": "Arrange the halogens in order of decreasing boiling point, starting with the highest and ending with the lowest.",
            "explanation": "Boiling points increase down the group due to stronger van der Waals forces in larger atoms."
        }
    ]

    
    current_property_index = 0
    current_property = properties[current_property_index]
    elements = [
        {"name": halogen, "rect": pygame.Rect(WIDTH // 2 - 300 + i * 120, HEIGHT // 2 - 25, 100, 50), "dragging": False, "placed": False, "correct": False, "speed": [random.choice([-1, 1]), random.choice([-1, 1])]} 
        for i, halogen in enumerate(current_property["order"])
    ]
    targets = [
        pygame.Rect(WIDTH // 2 - 300 + i * 120, HEIGHT // 2 + 100, 100, 50)
        for i in range(len(current_property["order"]))
    ]

    def draw_background():
        """Draw the game background."""
        screen.blit(background, (0, 0))

    def draw_elements():
        """Draw draggable elements."""
        for element in elements:
            color = GREEN if element["correct"] else (RED if element["placed"] else BABY_BLUE)
            pygame.draw.rect(screen, color, element["rect"])
            text = element_font.render(element["name"], True, BLACK)
            text_rect = text.get_rect(center=element["rect"].center)
            screen.blit(text, text_rect)

    def draw_targets():
        """Draw target areas."""
        for i, target in enumerate(targets):
            pygame.draw.rect(screen, RED, target, 2)

    def draw_instructions_and_explanation():
        """Draw instructions and explanations for the current property."""
        # Render instructions at the top center
        instruction_lines = textwrap.wrap(current_property["instruction"], width=60)
        instruction_box_height = len(instruction_lines) * 50 + 20
        instruction_box = pygame.Rect(
            WIDTH // 2 - 500, 10, 1000, instruction_box_height
        )
        pygame.draw.rect(screen, BLACK, instruction_box)
        pygame.draw.rect(screen, WHITE, instruction_box, 5)

        for i, line in enumerate(instruction_lines):
            instruction_text = instruction_font.render(line, True, WHITE)
            text_rect = instruction_text.get_rect(center=(WIDTH // 2, 40 + i * 50))
            screen.blit(instruction_text, text_rect)

        # Render explanations at the bottom center
        explanation_lines = textwrap.wrap(current_property["explanation"], width=60)
        explanation_box_height = len(explanation_lines) * 50 + 20
        explanation_box = pygame.Rect(
            WIDTH // 2 - 500, HEIGHT - 60 - explanation_box_height, 1000, explanation_box_height
        )
        pygame.draw.rect(screen, BLACK, explanation_box)
        pygame.draw.rect(screen, WHITE, explanation_box, 5)

        for i, line in enumerate(explanation_lines):
            explanation_text = instruction_font.render(line, True, WHITE)
            text_rect = explanation_text.get_rect(
                center=(WIDTH // 2, HEIGHT - 40 - explanation_box_height + 20 + i * 50)
            )
            screen.blit(explanation_text, text_rect)

    def move_elements():
        """Move elements around the screen."""
        for element in elements:
            if not element["dragging"] and not element["placed"]:
                element["rect"].x += element["speed"][0]
                element["rect"].y += element["speed"][1]

                if element["rect"].left < 0 or element["rect"].right > WIDTH:
                    element["speed"][0] *= -1
                if element["rect"].top < 0 or element["rect"].bottom > HEIGHT:
                    element["speed"][1] *= -1

    def check_completion():
        """Check if the elements are sorted correctly."""
        for i, element in enumerate(elements):
            if not targets[i].collidepoint(element["rect"].center) or not element["correct"]:
                return False
        return True

    # Game loop
    running = True
    while running:
        screen.fill(WHITE)
        draw_background()
        move_elements()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "exit"

            # Handle mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for element in elements:
                    if element["rect"].collidepoint(event.pos) and not element["placed"]:
                        element["dragging"] = True

            elif event.type == pygame.MOUSEBUTTONUP:
                for i, element in enumerate(elements):
                    if element["dragging"]:
                        element["dragging"] = False
                        if targets[i].collidepoint(element["rect"].center):
                            if element["name"] == current_property["order"][i]:
                                element["rect"].center = targets[i].center
                                element["placed"] = True
                                element["correct"] = True
                                correct_sound.play()  # Play sound on correct placement
                            else:
                                element["placed"] = True
                                element["correct"] = False

            elif event.type == pygame.MOUSEMOTION:
                for element in elements:
                    if element["dragging"]:
                        element["rect"].x += event.rel[0]
                        element["rect"].y += event.rel[1]

        # Draw game elements
        draw_elements()
        draw_targets()
        draw_instructions_and_explanation()

        # Check if the player has completed the current property sorting
        if check_completion():
            current_property_index += 1
            if current_property_index >= len(properties):
                print("Game completed!")
                return "finished"
            else:
                current_property = properties[current_property_index]
                elements = [
                    {"name": halogen, "rect": pygame.Rect(WIDTH // 2 - 300 + i * 120, HEIGHT // 2 - 25, 100, 50), "dragging": False, "placed": False, "correct": False, "speed": [random.choice([-1, 1]), random.choice([-1, 1])]} 
                    for i, halogen in enumerate(current_property["order"])
                ]

        # Update display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

def main():
    while True:
        result = halogen_sorting_game()
        print(f"Result from halogen_sorting_game: {result}")
        
        if result == "exit":
            break
    main()
def lanthanides_actinides_info():
    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Lanthanides and Actinides Info")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (70, 130, 180)
    RED = (255, 0, 0)

   
    content_font = pygame.font.Font("E:\\python\\Berthany.otf", 36)
    button_font = pygame.font.Font(None, 36)

    background = pygame.image.load("E:\\python\\map\\lantha ide.webp")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Lanthanides and Actinides content
    content = {
        "Lanthanides": "Lanthanides are the 15 elements with atomic numbers 57 through 71, starting from lanthanum. "
                       "They are often referred to as rare earth elements and are known for their high magnetic and optical properties.",
        "Details": "1. Found in the f-block of the periodic table.\n"
                   "2. Includes cerium, neodymium, europium, and more.\n"
                   "3. Known for their ability to absorb neutrons, making them valuable in nuclear technology.\n"
                   "4. Many are used in the production of strong magnets and lasers.",
        "Actinides": "Actinides are the 15 elements with atomic numbers 89 through 103, starting from actinium. "
                     "These elements are known for their radioactive properties and are mostly synthetic.",
        "Details": "1. Includes uranium, thorium, plutonium, and more.\n"
                   "2. Uranium and plutonium are key elements used in nuclear reactors and weapons.\n"
                   "3. Many actinides have applications in medical imaging and cancer treatment.\n"
                   "4. Actinides are highly reactive and require special handling due to their radioactivity.",
        "Storage and Safety": "1. Lanthanides are generally stable and safe under normal conditions.\n"
                              "2. Actinides must be stored in shielded containers to protect against radiation.\n"
                              "3. Proper ventilation is needed to avoid inhalation of radioactive particles.",
        "Fun Facts": "1. Neodymium is used in the strongest permanent magnets on Earth.\n"
                     "2. Europium is used in the red phosphors in TV and computer screens.\n"
                     "3. Uranium was once used in glassmaking to produce a fluorescent green color.\n"
                     "4. Americium is commonly found in smoke detectors.\n"
                     "5. Thorium can be used as an alternative fuel in nuclear reactors."
    }

    # Text box variables
    scroll_offset = 0
    scroll_speed = 10
    padding = 20  # Padding around text in the box

    # Preprocess content into wrapped lines
    wrapped_lines = []
    for section, text in content.items():
        wrapped_lines.append(f"{section}:")
        wrapped_lines.extend(textwrap.wrap(text, width=70))
        wrapped_lines.append("")  # Add spacing between sections

    # Calculate total content dimensions
    line_height = content_font.size("A")[1]
    content_width = max(content_font.size(line)[0] for line in wrapped_lines) + 2 * padding
    content_height = len(wrapped_lines) * line_height + 2 * padding

   
    box_width = min(content_width, WIDTH - 100)
    box_height = min(content_height, HEIGHT - 100)
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2


    button_width, button_height = 50, 30
    button_x, button_y = WIDTH - button_width - 10, 10
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # Game loop
    running = True
    while running:
        screen.blit(background, (0, 0))

        
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(screen, BLUE, box_rect)
        pygame.draw.rect(screen, BLACK, box_rect, 2)

        
        pygame.draw.rect(screen, RED, button_rect)
        text_surface = button_font.render("X", True, WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_DOWN:
                    scroll_offset = min(scroll_offset + scroll_speed, max(0, content_height - box_height + padding))
                elif event.key == pygame.K_UP:
                    scroll_offset = max(scroll_offset - scroll_speed, 0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False

        # Render text
        y = box_y + padding - scroll_offset
        for line in wrapped_lines:
            if y + line_height > box_y + padding and y < box_y + box_height - padding:
                text_surface = content_font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, y + line_height // 2))
                screen.blit(text_surface, text_rect)
            y += line_height

        # Update the display
        pygame.display.flip()
def lanthanides_actinides_trivia_adventure():
    pygame.init()

    # Screen dimensions and fullscreen
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Lanthanides & Actinides Trivia Adventure")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (93, 63, 211)
    EXIT_BUTTON_COLOR = (255, 69, 0)

   
    font = pygame.font.Font("E:\\python\\Berthany.otf", 40)

    # Load background
    background = pygame.image.load("E:\\python\\map\\lantha ide.webp")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Load sounds
    correct_sound = pygame.mixer.Sound("E:\\python\\correct_sound.wav.wav")
    wrong_sound = pygame.mixer.Sound("E:\\python\\wronganswer-37702.mp3")
    end_game_sound = pygame.mixer.Sound("E:\\python\\goodresult-82807.mp3")

    # Trivia Questions
    questions = [
        {"question": "Which lanthanide is used in lighter flints?", "options": ["Cerium", "Neodymium", "Europium", "Samarium"], "answer": "Cerium"},
        {"question": "Which actinide is used as nuclear fuel?", "options": ["Uranium", "Plutonium", "Thorium", "Neptunium"], "answer": "Uranium"},
        {"question": "Which lanthanide is known for its use in magnets?", "options": ["Dysprosium", "Neodymium", "Gadolinium", "Terbium"], "answer": "Neodymium"},
        {"question": "Which actinide is used in smoke detectors?", "options": ["Americium", "Plutonium", "Curium", "Berkelium"], "answer": "Americium"},
        {"question": "Which lanthanide has the highest atomic number?", "options": ["Lutetium", "Ytterbium", "Thulium", "Erbium"], "answer": "Lutetium"},
        {"question": "Which actinide is synthetic and highly radioactive?", "options": ["Californium", "Einsteinium", "Fermium", "Mendelevium"], "answer": "Fermium"},
    ]

    current_question_index = 0
    score = 0
    selected_option = None
    showing_feedback = False
    feedback_timer = 0

   
    exit_button_rect = pygame.Rect(WIDTH - 50, 10, 40, 40)

    
    def draw_text_box(text, x, y, width, height, text_color, box_color, border_color=None, border_width=0):
        box_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, box_color, box_rect)
        if border_color and border_width > 0:
            pygame.draw.rect(screen, border_color, box_rect, border_width)

        lines = text.split('\n')
        line_height = font.get_linesize()
        total_text_height = line_height * len(lines)
        start_y = y + (height - total_text_height) // 2

        for i, line in enumerate(lines):
            rendered_text = font.render(line, True, text_color)
            text_rect = rendered_text.get_rect(center=(x + width // 2, start_y + i * line_height + line_height // 2))
            screen.blit(rendered_text, text_rect)

    # Start screen
    def start_screen():
        running = True
        while running:
            screen.fill(WHITE)
            screen.blit(background, (0, 0))

            draw_text_box(
                "Welcome to Lanthanides & Actinides Trivia Adventure!\n\nRules:\n1. Answer the trivia questions.\n2. Correct answers give +10 points.\n3. Wrong answers subtract 5 points.\n4. Click 'Start' to begin!",
                WIDTH // 2 - 400, HEIGHT // 2 - 250, 800, 300, WHITE, BLUE, BLACK, 2
            )

            start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)
            pygame.draw.rect(screen, GREEN, start_button_rect)
            pygame.draw.rect(screen, WHITE, start_button_rect, 2)
            draw_text_box("Start", start_button_rect.x, start_button_rect.y, start_button_rect.width, 50, WHITE, GREEN)

            pygame.draw.rect(screen, EXIT_BUTTON_COLOR, exit_button_rect)
            pygame.draw.rect(screen, BLACK, exit_button_rect, 2)
            draw_text_box("X", exit_button_rect.x, exit_button_rect.y, 40, 40, WHITE, EXIT_BUTTON_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button_rect.collidepoint(event.pos):
                        running = False
                    elif exit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()

    # Main game logic
    result = start_screen()
    if result == "exit":
        return  # Return to the map

    running = True
    while running:
        screen.blit(background, (0, 0))
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos):
                    return

                if not showing_feedback and "feedback_rects" in locals():
                    for i, rect in enumerate(feedback_rects):
                        if rect.collidepoint(event.pos):
                            selected_option = i
                            correct_option = questions[current_question_index]["options"].index(questions[current_question_index]["answer"])
                            if selected_option == correct_option:
                                score += 10
                                correct_sound.play()
                            else:
                                score -= 5
                                wrong_sound.play()
                            showing_feedback = True
                            feedback_timer = current_time + 2000

        if current_question_index < len(questions):
            current_question = questions[current_question_index]
            draw_text_box(
                current_question["question"],
                WIDTH // 2 - 400, HEIGHT // 2 - 200, 800, 100, WHITE, BLUE, BLACK, 2
            )

            feedback_rects = []
            correct_option = current_question["options"].index(current_question["answer"])
            for i, option in enumerate(current_question["options"]):
                option_rect = pygame.Rect(WIDTH // 2 - 400, HEIGHT // 2 - 50 + i * 70, 800, 50)
                if showing_feedback:
                    if i == selected_option and i != correct_option:
                        color = RED
                    elif i == correct_option:
                        color = GREEN
                    else:
                        color = BLUE
                else:
                    color = BLUE
                pygame.draw.rect(screen, color, option_rect)
                pygame.draw.rect(screen, BLACK, option_rect, 2)
                draw_text_box(option, option_rect.x, option_rect.y, option_rect.width, 50, WHITE, color)
                feedback_rects.append(option_rect)

            if showing_feedback and current_time > feedback_timer:
                showing_feedback = False
                selected_option = None
                current_question_index += 1

        else:
            draw_text_box(
                f"Game Over!\nYour Score: {score}/{len(questions) * 10}",
                WIDTH // 2 - 400, HEIGHT // 2 - 200, 800, 200, WHITE, GREEN if score > 0 else RED, BLACK, 2
            )
            end_game_sound.play()

        draw_text_box(f"Score: {score}", 10, 10, 200, 50, BLACK, WHITE)

        pygame.draw.rect(screen, EXIT_BUTTON_COLOR, exit_button_rect)
        pygame.draw.rect(screen, BLACK, exit_button_rect, 2)
        draw_text_box("X", exit_button_rect.x, exit_button_rect.y, 40, 40, WHITE, EXIT_BUTTON_COLOR)

        pygame.display.flip()

    pygame.quit()
def alcsorting_mini_game():
    # Initialize Pygame
    pygame.init()

    # Screen settings
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Sorting Mini-Game: Alkaline Earth, Lanthanides, Actinides")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (100, 149, 237)
    GREEN = (34, 139, 34)
    RED = (220, 20, 60)
    BABY_BLUE = (137, 207, 240)

    instruction_font = pygame.font.Font("E:\\python\\Berthany.otf", 40)
    element_font = pygame.font.Font(None, 36)


    background = pygame.image.load("E:\\python\\map\\lantha ide.webp")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Load sound effect
    correct_sound = pygame.mixer.Sound("E:\\python\\map\\alkaline\\dnm\\correct_sound.wav.wav")

  
    properties = [
        {
            "name": "Atomic Radius (Lanthanides)",
            "order": ["La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu"],
            "instruction": "Arrange the lanthanides in order of decreasing atomic radius.",
            "explanation": "Atomic radius decreases across the lanthanide series due to the lanthanide contraction."
        },
        {
            "name": "Oxidation States (Actinides)",
            "order": ["Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr"],
            "instruction": "Arrange the actinides in order of most common oxidation states.",
            "explanation": "Oxidation states vary across actinides, but they generally increase with atomic number before stabilizing."
        }
    ]

    # Game variables
    current_property_index = 0
    current_property = properties[current_property_index]
    elements = [
        {"name": metal, "rect": pygame.Rect(WIDTH // 2 - 300 + i * 120, HEIGHT // 2 - 25, 100, 50), "dragging": False, "placed": False, "correct": False, "speed": [random.choice([-1, 1]), random.choice([-1, 1])]} 
        for i, metal in enumerate(current_property["order"][:6])
    ]
    targets = [
        pygame.Rect(WIDTH // 2 - 300 + i * 120, HEIGHT // 2 + 100, 100, 50)
        for i in range(len(elements))
    ]

    def draw_background():
        """Draw the game background."""
        screen.blit(background, (0, 0))

    def draw_elements():
        """Draw draggable elements."""
        for element in elements:
            color = GREEN if element["correct"] else (RED if element["placed"] else BABY_BLUE)
            pygame.draw.rect(screen, color, element["rect"])
            text = element_font.render(element["name"], True, WHITE)
            text_rect = text.get_rect(center=element["rect"].center)
            screen.blit(text, text_rect)

    def draw_targets():
        """Draw target areas."""
        for target in targets:
            pygame.draw.rect(screen, RED, target, 2)

    def draw_instructions_and_explanation():
        """Draw instructions and explanations for the current property."""
        instruction_lines = textwrap.wrap(current_property["instruction"], width=60)
        explanation_lines = textwrap.wrap(current_property["explanation"], width=60)

        for i, line in enumerate(instruction_lines):
            instruction_text = instruction_font.render(line, True, WHITE)
            instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, 50 + i * 40))
            screen.blit(instruction_text, instruction_rect)

        for i, line in enumerate(explanation_lines):
            explanation_text = instruction_font.render(line, True, WHITE)
            explanation_rect = explanation_text.get_rect(center=(WIDTH // 2, HEIGHT - 150 + i * 40))
            screen.blit(explanation_text, explanation_rect)

    def move_elements():
        """Move elements around the screen."""
        for element in elements:
            if not element["dragging"] and not element["placed"]:
                element["rect"].x += element["speed"][0]
                element["rect"].y += element["speed"][1]

                if element["rect"].left < 0 or element["rect"].right > WIDTH:
                    element["speed"][0] *= -1
                if element["rect"].top < 0 or element["rect"].bottom > HEIGHT:
                    element["speed"][1] *= -1

    def check_completion():
        """Check if the elements are sorted correctly."""
        for i, element in enumerate(elements):
            if not targets[i].collidepoint(element["rect"].center) or not element["correct"]:
                return False
        return True

    # Game loop
    running = True
    while running:
        screen.fill(WHITE)
        draw_background()
        move_elements()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "exit"

            # Handle mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for element in elements:
                    if element["rect"].collidepoint(event.pos) and not element["placed"]:
                        element["dragging"] = True

            elif event.type == pygame.MOUSEBUTTONUP:
                for i, element in enumerate(elements):
                    if element["dragging"]:
                        element["dragging"] = False
                        if targets[i].collidepoint(element["rect"].center):
                            if element["name"] == current_property["order"][i]:
                                element["rect"].center = targets[i].center
                                element["placed"] = True
                                element["correct"] = True
                                correct_sound.play()  # Play sound on correct placement
                            else:
                                element["placed"] = True
                                element["correct"] = False

            elif event.type == pygame.MOUSEMOTION:
                for element in elements:
                    if element["dragging"]:
                        element["rect"].x += event.rel[0]
                        element["rect"].y += event.rel[1]

        # Draw game elements
        draw_elements()
        draw_targets()
        draw_instructions_and_explanation()

        # Check if the player has completed the current property sorting
        if check_completion():
            current_property_index += 1
            if current_property_index >= len(properties):
                print("Game completed!")
                return "finished"
            else:
                current_property = properties[current_property_index]
                elements = [
                    {"name": metal, "rect": pygame.Rect(WIDTH // 2 - 300 + i * 120, HEIGHT // 2 - 25, 100, 50), "dragging": False, "placed": False, "correct": False, "speed": [random.choice([-1, 1]), random.choice([-1, 1])]} 
                    for i, metal in enumerate(current_property["order"][:len(targets)])
                ]

        # Update display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

def main():
    while True:
        result = alcsorting_mini_game()
        print(f"Result from sorting_mini_game: {result}")
        
        if result == "exit":
            break
    main()
# Functions for each game
def run_game(kingdom_number, game_number):
    if kingdom_number == 1 and game_number == 1:
        show_alkali_metals_info()
    elif kingdom_number == 1 and game_number == 2:
     alkali_metal_reactions_game()
    elif kingdom_number == 1 and game_number == 3:
        flame_test_colors_game()
    elif kingdom_number == 1 and game_number == 4:
       alkali_metals_sorting_game()
    elif kingdom_number == 2 and game_number == 1:
        alkaline_info()
    elif kingdom_number == 2 and game_number == 2:
        alflame()
    elif kingdom_number == 2 and game_number == 3:
        radioactive_maze_game()
    elif kingdom_number == 2 and game_number == 4:
        alkaline_earth_metals_sorting_game()
    elif kingdom_number == 3 and game_number == 1:
        run_noble_gas_info()
    elif kingdom_number == 3 and game_number == 2:
        noble_gas_trivia_adventure()
    elif kingdom_number == 3 and game_number == 3:
        run_element_catcher_game()
    elif kingdom_number == 3 and game_number == 4:
        noble_gases_sorting_game()
    elif kingdom_number == 4 and game_number == 1:
        transition_metals_info()
    elif kingdom_number == 4 and game_number == 2:
        transition_metals_trivia_adventure()
    elif kingdom_number == 5 and game_number == 1:
       run_halogen_info()
    elif kingdom_number == 5 and game_number == 2:
         halogen_trivia_adventure()
    elif kingdom_number == 5 and game_number == 3:
         run_halogen_defense()
    elif kingdom_number == 5 and game_number == 4:
         halogen_sorting_game()
    elif kingdom_number == 6 and game_number == 1:
         lanthanides_actinides_info()
    elif kingdom_number == 6 and game_number == 2:
          lanthanides_actinides_trivia_adventure()
    elif kingdom_number == 6 and game_number == 3:
         alcsorting_mini_game()
    
    else:
        display_game_screen(f"Game {game_number} in Kingdom {kingdom_number}")

def display_game_screen(message):
    running = True
    while running:
        screen.fill((50, 50, 50))  # Background color for the game
        text = pygame.font.Font("E:\\python\\Berthany.otf", 48).render(message, True, (255, 255, 255))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2,
                           screen.get_height() // 2 - text.get_height() // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
def show_alkali_metals_info():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Alkali Metals Info")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BROWN = (110, 38, 14)
    RED = (255, 0, 0)


    content_font = pygame.font.Font("E:\\python\\Berthany.otf", 36)
    button_font = pygame.font.Font("E:\\python\\Berthany.otf", 40)

    background = pygame.image.load("E:\\python\\map\\alkile.webp")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    content = {
        "Introduction": "Alkali metals are the elements in Group 1 of the periodic table. "
                        "They are highly reactive and have unique properties such as low melting points and soft textures.",
        "Details": "1. Found in Group 1 of the periodic table.\n"
                   "2. Soft, silvery metals that can be cut with a knife.\n"
                   "3. Extremely reactive, especially with water and oxygen.\n"
                   "4. Includes lithium, sodium, potassium, rubidium, cesium, and francium.",
        "Important Information": "1. Alkali metals have one valence electron, making them highly reactive.\n"
                                  "2. They react violently with water to form hydrogen gas and an alkali solution.\n"
                                  "3. These metals are never found in their free state in nature.\n"
                                  "4. Francium is radioactive and the rarest alkali metal.",
        "Storage and Safety": "1. Alkali metals must be stored in oil or inert atmospheres to prevent contact with moisture and oxygen.\n"
                              "2. Exposure to air can cause rapid oxidation and combustion.\n"
                              "3. Always handle with care, using protective equipment and avoiding direct contact with water.",
        "Usage": "1. Lithium is widely used in batteries and psychiatric medication.\n"
                 "2. Sodium is essential in table salt (sodium chloride) and street lighting.\n"
                 "3. Potassium is vital for fertilizers and biological processes.\n"
                 "4. Cesium is used in atomic clocks for its precision.",
        "Fun Facts": "1. Sodium and potassium are essential for nerve function in humans.\n"
                     "2. Cesium is one of the most expensive metals and is used in drilling fluids.\n"
                     "3. Francium is so rare that its total quantity on Earth is estimated to be less than 30 grams.\n"
                     "4. Alkali metals are highly flammable and must be handled with extreme caution."
    }

    # Text box variables
    scroll_offset = 0
    scroll_speed = 10
    padding = 20  # Padding around text in the box

    # Preprocess content into wrapped lines
    wrapped_lines = []
    for section, text in content.items():
        wrapped_lines.append(f"{section}:")
        wrapped_lines.extend(textwrap.wrap(text, width=70))
        wrapped_lines.append("")  # Add spacing between sections

    # Calculate total content dimensions
    line_height = content_font.size("A")[1]
    content_width = max(content_font.size(line)[0] for line in wrapped_lines) + 2 * padding
    content_height = len(wrapped_lines) * line_height + 2 * padding


    box_width = min(content_width, WIDTH - 100)
    box_height = min(content_height, HEIGHT - 100)
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2

   
    button_width, button_height = 40, 40
    exit_button = pygame.Rect(WIDTH - 50, 10, button_width, button_height)  # Draw exit button (brown cross)

    # Game loop
    running = True
    while running:
        screen.blit(background, (0, 0))

        
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(screen, BROWN, box_rect)
        pygame.draw.rect(screen, BLACK, box_rect, 2)

        
        pygame.draw.rect(screen, BROWN, exit_button)  
        cross_text = button_font.render("X", True, WHITE) 
        screen.blit(cross_text, (exit_button.centerx - cross_text.get_width() // 2, exit_button.centery - cross_text.get_height() // 2))

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_DOWN:
                    scroll_offset = min(scroll_offset + scroll_speed, max(0, content_height - box_height + padding))
                elif event.key == pygame.K_UP:
                    scroll_offset = max(scroll_offset - scroll_speed, 0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):  # Check if the exit button is clicked
                    running = False

        # Render text
        y = box_y + padding - scroll_offset
        for line in wrapped_lines:
            if y + line_height > box_y + padding and y < box_y + box_height - padding:
                text_surface = content_font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, y + line_height // 2))
                screen.blit(text_surface, text_rect)
            y += line_height

        # Update the display
        pygame.display.flip()
def alkali_metal_reactions_game():
    # Initialize Pygame
    pygame.init()

    # Screen settings (full-screen mode)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_width(), screen.get_height()
    pygame.display.set_caption("Alkali Metal Reactions")

    # Font settings - use Berthany.otf for all text
    font_path = "E:\\python\\map\\Berthany.otf"
    font = pygame.font.Font(font_path, 60)  # Larger font for instructions
    label_font = pygame.font.Font(font_path, 40)  # Larger font for labels

    # Load background
    background = pygame.image.load("E:\\python\\reaction\\alkali reaction\\lakeinvolcanicland.webp").convert_alpha()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Load jars image
    jar_image = pygame.image.load("E:\\python\\reaction\\alkali reaction\\file (2).png").convert_alpha()
    jar_image = pygame.transform.scale(jar_image, (150, 200))  # Increase the size of the jars

    # Load metal images
    metals = {
        "Li": pygame.image.load("E:\\python\\reaction\\alkali reaction\\Lithium.png").convert_alpha(),
        "Na": pygame.image.load("E:\\python\\reaction\\alkali reaction\\Na.png").convert_alpha(),
        "K": pygame.image.load("E:\\python\\reaction\\alkali reaction\\k.png").convert_alpha(),
        "Rb": pygame.image.load("E:\\python\\reaction\\alkali reaction\\Rb.png").convert_alpha(),
        "Cs": pygame.image.load("E:\\python\\reaction\\alkali reaction\\Cs.png").convert_alpha(),
        "Fr": pygame.image.load("E:\\python\\reaction\\alkali reaction\\Fr.png").convert_alpha(),
    }

    # Resize metal images
    for key in metals:
        metals[key] = pygame.transform.scale(metals[key], (60, 60))  # Increase size of elements

    # Load sounds
    sounds = {
        "Li": pygame.mixer.Sound("E:\\python\\reaction\\alkali reaction\\lisound (3).wav"),
        "Na": pygame.mixer.Sound("E:\\python\\reaction\\alkali reaction\\nasound.wav"),
        "K": pygame.mixer.Sound("E:\\python\\reaction\\alkali reaction\\ksound (1).wav"),
        "Rb": pygame.mixer.Sound("E:\\python\\reaction\\alkali reaction\\ksound (1).wav"),
        "Cs": pygame.mixer.Sound("E:\\python\\reaction\\alkali reaction\\ksound (1).wav"),
        "Fr": pygame.mixer.Sound("E:\\python\\reaction\\alkali reaction\\Fr.wav"),
    }

    # Centered jar positions with equal spacing
    jar_spacing = 160
    starting_x = WIDTH // 2 - (jar_spacing * 2.5)  # Adjusted for 6 jars
    jar_positions = [(starting_x + i * jar_spacing, HEIGHT - 250) for i in range(6)]
    element_names = list(metals.keys())

    # Reaction box settings (horizontal oval)
    REACTION_BOX_RECT = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 100)  # x, y, width, height

    # Chemical reactions
    chemical_reactions = {
        "Li": "Li + H2O -> LiOH + H2",
        "Na": "Na + H2O -> NaOH + H2",
        "K": "K + H2O -> KOH + H2",
        "Rb": "Rb + H2O -> RbOH + H2",
        "Cs": "Cs + H2O -> CsOH + H2",
        "Fr": "Fr + H2O -> FrOH + H2",
    }

    # Particle class
    class Particle:
        def __init__(self, x, y, x_vel, y_vel, size, color, lifetime):
            self.x = x
            self.y = y
            self.x_vel = x_vel
            self.y_vel = y_vel
            self.size = size
            self.color = color
            self.lifetime = lifetime

        def update(self):
            self.x += self.x_vel
            self.y += self.y_vel
            self.size *= 0.95  # Shrink particle over time
            self.lifetime -= 1

        def draw(self, screen):
            if self.lifetime > 0:
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

    # Particle effects
    particles = []

    # Reaction effects
    reactions = {
        "Li": {"fire": 20, "smoke": 0, "color": (255, 150, 0), "multiplier": 1, "lifetime": 60},
        "Na": {"fire": 30, "smoke": 80, "color": (255, 255, 0), "multiplier": 1, "lifetime": 160},
        "K": {"fire": 40, "smoke": 70, "color": (255, 100, 0), "multiplier": 3, "lifetime": 180},
        "Rb": {"fire": 50, "smoke": 100, "color": (255, 50, 0), "multiplier": 4, "lifetime": 200},
        "Cs": {"fire": 60, "smoke": 120, "color": (255, 0, 0), "multiplier": 5, "lifetime": 220},
        "Fr": {"fire": 80, "smoke": 150, "color": (255, 150, 0), "multiplier": 6, "lifetime": 250},
    }

   
    dragging = None
    metal_positions = {key: (pos[0] + 45, pos[1] + 75) for key, pos in zip(metals.keys(), jar_positions)}

 
    reaction_message = ""
    reaction_timer = 0

   
    exit_button = pygame.Rect(WIDTH - 50, 5, 50, 50)


    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

       
        instruction_text = font.render("Drag the elements in the lake and drop them in the circle to see the reactions", True, (255, 255, 255))
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, 20))

       
        for i, pos in enumerate(jar_positions):
            screen.blit(jar_image, pos)
            metal_key = element_names[i]
            screen.blit(metals[metal_key], metal_positions[metal_key])
            label = label_font.render(metal_key, True, (255, 255, 255))  
            screen.blit(label, (pos[0] + jar_image.get_width() // 2 - label.get_width() // 2, pos[1] + jar_image.get_height() + 10))

      
        pygame.draw.ellipse(screen, (72, 191, 145), REACTION_BOX_RECT, 2)

        
        pygame.draw.rect(screen, (139, 69, 19), exit_button) 
        exit_text = font.render("X", True, (255, 255, 255))
        screen.blit(exit_text, (exit_button.x + (exit_button.width - exit_text.get_width()) // 2, 
                                exit_button.y + (exit_button.height - exit_text.get_height()) // 2))

        if reaction_message and reaction_timer > 0:
            reaction_text = font.render(reaction_message, True, (255, 255, 255))
            screen.blit(reaction_text, (WIDTH // 2 - reaction_text.get_width() // 2, HEIGHT // 4))
            reaction_timer -= 1

       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    running = False 
                for key, pos in metal_positions.items():
                    rect = pygame.Rect(pos[0], pos[1], 60, 60)
                    if rect.collidepoint(event.pos):
                        dragging = key
                        break
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    if REACTION_BOX_RECT.collidepoint(event.pos):
                        sounds[dragging].play()
                        reaction = reactions[dragging]
                        for _ in range(reaction["fire"] * reaction["multiplier"]):
                            particles.append(Particle(event.pos[0], event.pos[1],
                                                      random.uniform(-2, 2), random.uniform(-5, -1),
                                                      random.uniform(5, 10), reaction["color"], reaction["lifetime"]))
                        for _ in range(reaction["smoke"]):
                            particles.append(Particle(event.pos[0], event.pos[1],
                                                      random.uniform(-2, 2), random.uniform(-1, 0),
                                                      random.uniform(5, 15), (200, 200, 200), 80))
                        reaction_message = chemical_reactions[dragging]
                        reaction_timer = 180
                    metal_positions[dragging] = (jar_positions[element_names.index(dragging)][0] + 45,
                                                 jar_positions[element_names.index(dragging)][1] + 75)
                    dragging = None

        if dragging:
            pos = pygame.mouse.get_pos()
            metal_positions[dragging] = (pos[0] - 30, pos[1] - 30)

        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        pygame.display.flip()
        clock.tick(60)

running = True
while running:
    screen.fill((255, 255, 255))  
    screen.blit(map_image, (0, 0))  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: 
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                handle_click(event.pos)
   
    pygame.display.flip()


running = True
while running:
    screen.fill((255, 255, 255))  
    screen.blit(map_image, (0, 0)) 

   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: 
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                handle_click(event.pos)
   
    pygame.display.flip()


pygame.quit()
