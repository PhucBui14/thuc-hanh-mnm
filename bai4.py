import pygame
import random
import math

# Khởi tạo Pygame
pygame.init()

# Thiết lập kích thước cửa sổ
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Bắn Chim")

# Màu sắc
BLACK = (0, 0, 0)

# Tốc độ chim
BIRD_SPEED = 5

# Tải hình ảnh con chim
bird_image = pygame.image.load("thuchanh\cird.png")
bird_image = pygame.transform.scale(bird_image, (50, 50))  # Đặt kích thước con chim

# Tải hình nền
background_image = pygame.image.load("thuchanh\hinhnen.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Điều chỉnh kích thước nền

# Khởi tạo đồng hồ
clock = pygame.time.Clock()

# Lớp Chim
class Bird:
    def __init__(self):
        self.size = 50
        self.alive = True
        self.hit = False  # Đánh dấu nếu chim bị bắn
        
        # Chim xuất hiện ngẫu nhiên ở bất kỳ cạnh nào của màn hình
        self.side = random.choice(['left', 'right', 'top', 'bottom'])
        if self.side == 'left':
            self.x = -self.size
            self.y = random.randint(0, HEIGHT)
        elif self.side == 'right':
            self.x = WIDTH + self.size
            self.y = random.randint(0, HEIGHT)
        elif self.side == 'top':
            self.x = random.randint(0, WIDTH)
            self.y = -self.size
        elif self.side == 'bottom':
            self.x = random.randint(0, WIDTH)
            self.y = HEIGHT + self.size

        # Tạo hướng bay ngẫu nhiên
        angle = random.uniform(0, 2 * math.pi)  # Góc ngẫu nhiên từ 0 đến 2*pi
        self.dx = BIRD_SPEED * math.cos(angle)
        self.dy = BIRD_SPEED * math.sin(angle)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        
        # Kiểm tra nếu chim bay ra ngoài màn hình theo chiều ngang hoặc dọc
        if (self.x < -self.size or self.x > WIDTH + self.size or 
            self.y < -self.size or self.y > HEIGHT + self.size):
            self.alive = False

    def draw(self, screen):
        if self.alive:
            # Vẽ hình con chim tại vị trí (self.x, self.y)
            screen.blit(bird_image, (int(self.x), int(self.y)))

# Game loop
def main():
    birds = []
    score = 0
    running = True

    while running:
        # Vẽ hình nền
        screen.blit(background_image, (0, 0))

        # Tạo chim mới với xác suất cao hơn để nhiều chim xuất hiện cùng lúc
        if random.randint(1, 8) == 1:  # Giảm khoảng cách thời gian để tăng số chim
            birds.append(Bird())

        # Vẽ chim và xử lý di chuyển
        for bird in birds[:]:
            if bird.alive:
                bird.move()
                bird.draw(screen)
            else:
                if bird.hit:
                    score += 1  # Chỉ cộng điểm nếu chim bị bắn
                birds.remove(bird)

        # Hiển thị điểm số
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Kiểm tra sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for bird in birds:
                    if bird.alive and (bird.x < mouse_pos[0] < bird.x + bird.size) and (bird.y < mouse_pos[1] < bird.y + bird.size):
                        bird.alive = False
                        bird.hit = True  # Đánh dấu chim đã bị bắn

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
