import pygame
import random
import math

# 初始化 Pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
CAT_RADIUS = 20
MOUSE_RADIUS = 10
INITIAL_MICE = 3

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GRAY = (200, 200, 200)


class Cat:
    """猫类 - 跟随鼠标移动"""
    
    def __init__(self):
        self.radius = CAT_RADIUS
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
    
    def update(self, mouse_pos):
        """根据鼠标位置更新猫的位置"""
        self.x = mouse_pos[0]
        self.y = mouse_pos[1]
    
    def draw(self, screen):
        """绘制猫"""
        pygame.draw.circle(screen, ORANGE, (self.x, self.y), self.radius)
        # 绘制眼睛
        pygame.draw.circle(screen, BLACK, (self.x - 7, self.y - 5), 3)
        pygame.draw.circle(screen, BLACK, (self.x + 7, self.y - 5), 3)
    
    def check_collision(self, other):
        """检测与其他对象的碰撞"""
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        return distance < self.radius + other.radius


class Mouse:
    """老鼠类 - 随机移动"""
    
    def __init__(self):
        self.radius = MOUSE_RADIUS
        self.x = random.randint(self.radius, SCREEN_WIDTH - self.radius)
        self.y = random.randint(self.radius, SCREEN_HEIGHT - self.radius)
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.change_direction_counter = 0
    
    def update(self):
        """更新老鼠的位置"""
        # 随机改变方向
        self.change_direction_counter += 1
        if self.change_direction_counter > 120:  # 每2秒改变一次方向
            self.vx = random.uniform(-3, 3)
            self.vy = random.uniform(-3, 3)
            self.change_direction_counter = 0
        
        # 更新位置
        self.x += self.vx
        self.y += self.vy
        
        # 边界反弹
        if self.x - self.radius < 0 or self.x + self.radius > SCREEN_WIDTH:
            self.vx = -self.vx
            self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
        
        if self.y - self.radius < 0 or self.y + self.radius > SCREEN_HEIGHT:
            self.vy = -self.vy
            self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.y))
    
    def draw(self, screen):
        """绘制老鼠"""
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)
        # 绘制尾巴
        tail_x = self.x - self.vx * 3
        tail_y = self.y - self.vy * 3
        pygame.draw.line(screen, RED, (self.x, self.y), (tail_x, tail_y), 2)


class Game:
    """游戏主类"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🐱 猫捉老鼠游戏 🐭")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 72)
        
        self.reset_game()
    
    def reset_game(self):
        """重置游戏"""
        self.cat = Cat()
        self.mice = [Mouse() for _ in range(INITIAL_MICE)]
        self.score = 0
        self.game_over = False
        self.win = False
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_r:
                    self.reset_game()
        return True
    
    def update(self):
        """更新游戏状态"""
        if self.game_over or self.win:
            return
        
        # 更新鼠标位置到猫的位置
        mouse_pos = pygame.mouse.get_pos()
        self.cat.update(mouse_pos)
        
        # 更新老鼠
        for mouse in self.mice:
            mouse.update()
        
        # 检测碰撞
        mice_to_remove = []
        for mouse in self.mice:
            if self.cat.check_collision(mouse):
                mice_to_remove.append(mouse)
                self.score += 10
        
        # 移除被捉住的老鼠
        for mouse in mice_to_remove:
            self.mice.remove(mouse)
        
        # 所有老鼠都被捉住则获胜
        if len(self.mice) == 0:
            self.win = True
            # 添加新的老鼠继续游戏
            for _ in range(INITIAL_MICE + self.score // 10):
                self.mice.append(Mouse())
    
    def draw(self):
        """绘制游戏画面"""
        self.screen.fill(LIGHT_GRAY)
        
        # 绘制猫和老鼠
        self.cat.draw(self.screen)
        for mouse in self.mice:
            mouse.draw(self.screen)
        
        # 绘制UI信息
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        mice_text = self.font.render(f"Mice: {len(self.mice)}", True, BLACK)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(mice_text, (10, 50))
        
        # 绘制获胜提示
        if self.win:
            win_text = self.font_large.render("YOU WIN!", True, GREEN)
            restart_text = self.font.render("Press R to continue, ESC to exit", True, BLACK)
            
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            
            # 绘制半透明背景
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            s.set_alpha(128)
            s.fill(BLACK)
            self.screen.blit(s, (0, 0))
            
            self.screen.blit(win_text, text_rect)
            self.screen.blit(restart_text, restart_rect)
            
            self.win = False  # 重置获胜状态
        
        pygame.display.flip()
    
    def run(self):
        """运行游戏主循环"""
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
