import pygame
import numpy as np
import math
import random

# Bouncing Balls Program
# Thực hiện chương trình theo thứ tự các bước
	# 1. Thiết lập Pygame
	# 2. Vẽ đường tròn và bóng
	# 3. Để bóng rơi tự do
	# 4. Thực hiện nảy bóng khi chạm vào đường tròn
	# 5. Hiệu ứng xoay vòng tròn
	# 6. Bóng ra khỏi vòng tròn và biến mất
	# 7. Tạo thêm bóng

# object Ball chứa các thuộc tính: tọa độ, vận tốc, màu sắc và sự nằm trong đường tròn
class Ball:
	def __init__(self, pos, vel):
		self.pos = np.array(pos, dtype=np.float64)
		self.v = np.array(vel, dtype=np.float64)
		self.color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
		self.is_in = True

# Vẽ một tam giác với 1 điểm là tâm đường tròn và cho xoay liên tục tạo hiệu ứng
def draw_arc(window, center, radius, start_angle, end_angle):
	p1 = center + (radius+1000) * np.array([math.cos(start_angle),math.sin(start_angle)])
	p2 = center + (radius+1000) * np.array([math.cos(end_angle),math.sin(end_angle)])
	pygame.draw.polygon(window, BLACK, [center,p1,p2], 0)

# Kiểm tra bóng rơi ra ngoài vòng tròn
def is_ball_in_circle(ball_pos, circle_center, start_angle, end_angle):
	dx = ball_pos[0] - circle_center[0]
	dy = ball_pos[1] - circle_center[1]
	ball_angle = math.atan2(dy, dx)
	end_angle = end_angle % (2 * math.pi)
	start_angle = start_angle % (2 * math.pi)
	if start_angle > end_angle:
		end_angle += 2 * math.pi
	if start_angle <= ball_angle <= end_angle or (start_angle <= ball_angle + 2 * math.pi <= end_angle):
		return True

# Bước 1: Thiết lập Pygame
pygame.init()
UI = pygame.display
UI.set_caption('Bounce Balls')

# Bước 2: Vẽ đường tròn và bóng
	# Tạo chiều dài và chiều rộng
width = 400
height = 400

	# Tạo cửa sổ
WINDOW = UI.set_mode((width, height))

clock = pygame.time.Clock()
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

	# Tạo tọa độ tâm và bán kính
CIRCLE_CENTER = np.array([width/2, height/2], dtype=np.float64)
CIRCLE_RADIUS = 150
BALL_RADIUS = 5

	# Tạo các thông số của tam giác: số đo góc ở tâm
CENTRAL_ANGLE = 60
START_ANGLE = math.radians( -CENTRAL_ANGLE/2)
END_ANGLE = math.radians( CENTRAL_ANGLE/2)

	# Tạo thông số quả bóng: tọa độ, vận tốc
position = np.array([width/2, height/2 - 120], dtype=np.float64)
velocity = np.array([0,0], dtype=np.float64)
balls = [Ball (position, velocity)]
ball_number = 100
while ball_number > 0:
	balls.append(Ball(pos=[width // 2, height // 2 - 120], vel=[random.uniform(-4, 4), random.uniform(-1, 1)]))
	ball_number = ball_number - 1

running = True
ACCELERATION = 0.2
spinning_speed = 0.01

# Bước 3: Để bóng rơi tự do
while running:
	# Điều kiện thoát
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# Tạo hiệu ứng xoay bằng cách thay đổi tọa độ các điểm của dây cung
	START_ANGLE += spinning_speed
	END_ANGLE += spinning_speed

	for ball in balls:

# Bước 6: Bóng ra khỏi cửa sổ và biến mất
# Bước 7: Tạo thêm bóng
	# Nếu 1 quả bóng k còn hiện trên cửa sổ thì tạo thêm quả bóng khác
		if ball.pos[0] < 0 or ball.pos[1] > height or ball.pos[0] > width or ball.pos[1] < 0:
			balls.remove(ball)
			balls.append(Ball(pos=[width // 2, height // 2 - 120], vel=[random.uniform(-4, 4),random.uniform(-1, 1)]))

# Bước 4: Thực hiện nảy bóng khi chạm vào đường tròn
		ball.v[1] += ACCELERATION
		ball.pos += ball.v
		ball_to_center_distance = np.linalg.norm(ball.pos - CIRCLE_CENTER) + BALL_RADIUS

		if ball_to_center_distance > CIRCLE_RADIUS:
			if is_ball_in_circle(ball.pos, CIRCLE_CENTER, START_ANGLE, END_ANGLE):
				ball.is_in = False

			if ball.is_in:

				# Vectơ chỉ phương của đường thẳng qua bóng và tâm
				d = ball.pos - CIRCLE_CENTER

				# Vectơ đơn vị và vectơ chỉ phương của tiếp tuyến
				d_unit = d/np.linalg.norm(d)
				t = np.array([-d[1],d[0]], dtype=np.float64)

				# Tọa độ hình chiếu vectơ bóng chạm vào đường tròn
				proj_v_t = (np.dot(ball.v,t)/np.dot(t,t)) * t

				# Tốc độ bóng nảy
				ball.v = 2 * proj_v_t - ball.v
				ball.v += t * spinning_speed

				# Vị trí hiện tại
				ball.pos = CIRCLE_CENTER + (CIRCLE_RADIUS - BALL_RADIUS) * d_unit

	WINDOW.fill(BLACK)
	pygame.draw.circle(WINDOW, ORANGE, CIRCLE_CENTER, CIRCLE_RADIUS, 3)

# Bước 5: Hiệu ứng xoay vòng tròn
	draw_arc(WINDOW, CIRCLE_CENTER, CIRCLE_RADIUS, START_ANGLE, END_ANGLE)

	for ball in balls:
		pygame.draw.circle(WINDOW, ball.color, ball.pos, BALL_RADIUS)

	UI.flip()
	clock.tick(60)
pygame.quit()