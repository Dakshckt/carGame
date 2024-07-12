import pygame
import random
import os
from database import updateScorce

class backSide:
    def __init__(self):
        self.WIDTH , self.HEIGHT = 900 , 600
        self.backgroundY1 = 0
        self.backgroundY2 = 0 - self.HEIGHT
        self.images()

    def images(self):
        self.background = pygame.image.load('./AllPhotos/Race-background.png')
        self.background = pygame.transform.scale(self.background , (self.WIDTH , self.HEIGHT))
        



class redCar:
    def __init__(self):
        self.carWidth , self.carHeight = 70 , 100
        self.speed = 1
        self.speed_inc = 0.4
        self.turn = 3
        self.move = 4
        self.images()
    
    def images(self):
        self.mainCar = pygame.image.load('./AllPhotos/redCar.png')
        self.mainCar = pygame.transform.scale(self.mainCar , (self.carWidth , self.carHeight))




def drawWindow(WIN , x,  y , game , car , obstacles , imgObstacles , point , highestScore):
    WIN.blit(game.background , (0,game.backgroundY1))
    WIN.blit(game.background , (0,game.backgroundY2))
    WIN.blit(car.mainCar , (x , y))

    for drawObstacles in imgObstacles:
        img = drawObstacles['images']
        sizeX = drawObstacles['sizeX']
        sizeY = drawObstacles['sizeY']
        WIN.blit(img , (sizeX , sizeY))
    
    font1 = pygame.font.SysFont('comicsans' , 30 , True)
    text1 = font1.render('Score : ' + str(point) , 1 , (0,0,0))
    text2 = font1.render('Highest Score : ' + str(highestScore) , 1 , (0,0,0))
    WIN.blit(text1 , (50 , 50))
    WIN.blit(text2 , (500 , 50))

    pygame.display.update()




def checkGeneration(existing_positions):
    car_width = 80
    while True:
        generated = random.randrange(190, 620)
        overlap = False
        for pos in existing_positions:
            if abs(generated - pos) < car_width:
                overlap = True
                break
        if not overlap:
            return generated
        
        
def gameOver(WIN ,highestScore , point):

    if point > int(highestScore):
        dataObj = updateScorce()
        result = dataObj.update(point)
        print(result)
        
    quitImageWidth , quitImageHeight = 120 , 50
    replayImageWidth , replayImageHeight = 320 , 50

    quitImageX ,quitImageY = 200 , 350
    replayImageX , replayImageY = 400 , 350

    gameOverImg = pygame.image.load('./AllPhotos/gameOver.webp')
    gameOverImg = pygame.transform.scale(gameOverImg , (400 , 300))
    text1 = pygame.image.load("./AllPhotos/playAgain.png")
    text2 = pygame.image.load("./AllPhotos/Quit.png")
    text1 = pygame.transform.scale(text1 , (replayImageWidth , replayImageHeight))
    text2 = pygame.transform.scale(text2 , (quitImageWidth , quitImageHeight))
    WIN.blit(text1 , (replayImageX , replayImageY))
    WIN.blit(text2 , (quitImageX ,quitImageY))
    WIN.blit(gameOverImg , (250 , 100))


    pygame.display.update()

    keys = pygame.key.get_pressed()

    replay = False
    while not replay:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                result = pygame.mouse.get_pos()
                mouseX = result[0]
                mouseY = result[1]

                if mouseX > quitImageX and mouseX < quitImageX + quitImageWidth and mouseY > quitImageY and quitImageY + quitImageHeight:
                    return False 
                elif mouseX > replayImageX and mouseX < replayImageX + replayImageWidth and mouseY > replayImageY and replayImageY + replayImageHeight:
                    return True       





def main(take):
    pygame.init()
    global backgroundY1 , backgroundY2
    run = True
    first = take
    if first == True:
        go = False
    if first == False:
        go = True
        
    point = 0


    game = backSide()
    car = redCar()
    databaseObj = updateScorce()
    highestScore = databaseObj.select()

    carCrash = pygame.mixer.Sound('./AllPhotos/car-crash.wav')
    carHorn = pygame.mixer.Sound('./AllPhotos/car-horn.wav')
    carMirrorBreak = pygame.mixer.Sound('./AllPhotos/window-break.wav')
    music = pygame.mixer.music.load('./AllPhotos/music.mp3')
    pygame.mixer.music.play(-1)

    obstacle_speed_increment = 2000
    obstacleHeight , obstacleWidth = 70 , 90
    obstacle_count = 0 
    obstacle_vel = 5
    obstacles = []
    imgObstacles = []
    obstacleImg = [
        pygame.transform.scale((pygame.image.load(os.path.join('AllPhotos' , 'greenObstacle.png'))) , (car.carWidth , car.carHeight)),
        pygame.transform.scale(pygame.image.load(os.path.join('AllPhotos' , 'yellowObstacle.png')), (car.carWidth , car.carHeight))
    ]

    x = 400
    y = 400

    FPS = 60


    WIN = pygame.display.set_mode((game.WIDTH , game.HEIGHT))

    clock = pygame.time.Clock()
    INCREASE_SPEED = pygame.USEREVENT + 1
    pygame.time.set_timer(INCREASE_SPEED , 2000)
    
    pygame.display.set_caption("Car Game")
    
    while run:

        try :
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            while first:
                startBackground = pygame.image.load('./AllPhotos/startBackground.jpg')
                startBackground = pygame.transform.scale(startBackground , (game.WIDTH , game.HEIGHT))
                startLetter = pygame.image.load('./AllPhotos/startPageLetter.png')
                startLetter = pygame.transform.scale(startLetter , (500 , 100))
                font1 = pygame.font.SysFont('comicsans' , 20 , True)
                text1 = font1.render('Press `s` to start the game' , 1 , (255,255,255))
                WIN.blit(startBackground , (0,0))
                WIN.blit(startLetter , (200 , 100))
                WIN.blit(text1 , (300 , 200))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        first = False
                        go = False
                        run = False
                    
                    if pygame.key.get_pressed()[pygame.K_s]:
                        go = True
                        first = False
                        main(take = first)
                        

            if go == True:
                inc = clock.tick(FPS)
                obstacle_count += inc

                for event in pygame.event.get():
                    if car.speed <= 20:
                        if event.type == INCREASE_SPEED:
                            car.speed += car.speed_inc
                
                if obstacle_count > obstacle_speed_increment:
                    select_range = 2
                    curr_position = []
                    for _ in range(select_range):
                        carX = checkGeneration(curr_position)
                        curr_position.append(carX)
                        carY = car.carHeight * -1
                        img = random.choice(obstacleImg)
                        obs = pygame.Rect(carX , carY ,obstacleHeight , obstacleWidth)
                        imageCarX = carX
                        imageCarY = carY
                        imgObstacles.append({'images' : img , 'sizeX' : imageCarX , 'sizeY' : imageCarY})
                        obstacles.append(obs)
                    
                    if obstacle_speed_increment == 540:
                        obstacle_speed_increment = 540
                    else:
                        obstacle_speed_increment -= 20
                    obstacle_count = 0



                if game.backgroundY1 >= game.HEIGHT:
                    game.backgroundY1 = game.backgroundY2 - game.HEIGHT
                if game.backgroundY2 >= game.HEIGHT:
                    game.backgroundY2 = game.backgroundY1 - game.HEIGHT

                keys = pygame.key.get_pressed()

                if car.speed >= 5:
                    car.turn = min(10, 5 + (car.speed - 1) // 3) 
                    obstacle_vel = min(10, 5 + (car.speed - 1) // 3) 


                if keys[pygame.K_LEFT] and x > 190:
                    x = x - car.turn
                if keys[pygame.K_RIGHT] and x < 620:
                    x = x + car.turn
                if keys[pygame.K_UP] and y > 300:
                    y = y - car.move
                if keys[pygame.K_DOWN] and y < 400:
                    y = y + car.move
                if keys[pygame.K_SPACE]:
                    carHorn.play()

                point += 1
                
                for obstacle in obstacles:
                    obstacle.y += obstacle_vel

                    if obstacle.y + obstacleHeight >= y and y + car.carWidth >= obstacle.y and obstacle.x + obstacleWidth-40 >= x and x + car.carWidth-20 >= obstacle.x:
                        res = random.choice([0 , 1])
                        
                        if res == 0:
                            carCrash.play()
                        elif res == 1:
                            carMirrorBreak.play()

                        result = gameOver(WIN ,highestScore , point)
                        if result == False:
                            first = True
                            go = False
                            main(take = True)
                        elif result == True:
                            run = True
                            main(take = False)
                    
                for drawObstacle in imgObstacles:
                    drawObstacle['sizeY'] = drawObstacle['sizeY'] + obstacle_vel
                
                game.backgroundY1 , game.backgroundY2 = game.backgroundY1 + car.speed , game.backgroundY2 + car.speed

                drawWindow(WIN , x , y , game , car  , obstacles , imgObstacles , point , highestScore)


        except Exception as err:
            print('Something is wrong' , str(err))
            run = False
            pygame.quit()


    pygame.quit()

if __name__ == '__main__':
    main(take = True)