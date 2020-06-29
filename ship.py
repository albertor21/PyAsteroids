import pygame
from pygame.locals import *
 

class Ship(pygame.sprite.Sprite):
    '''
    filename : name of the sprite sheet image file
    framesize: size (rect, 0,0, w, h) of each frame
    speed : framerate ( if 0 display current frame)
    frames : list of number frames
    once: display anim once
    done: anim terminated
    '''
    def __init__(self, filename, frame_size,speed, frames, once, frame, done = False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = (0,0)
        self.frame_size = frame_size
        self.speed = speed
        self.frames = frames
        self.currentFrame = 0;
        self.once = once
        self.done = done
        self.frame = frame
    #añadido para dibujar un solo frame a eleccion con el metodo setFrame(frame)
    
    def setCurrentFrame (frame):
        self.currentFrame = frame

    def update(self, dt):
        self.currentFrame += 1
        
    def render(self, rectangle):
        rect = pygame.Rect(rectangle)
        result_image = pygame.Surface(rect.size).convert_alpha()
        result_image.blit(self.image, (0, 0), rect)
        return result_image

        render: function (ctx) {
          var frame;
          if (this.speed > 0) {
            var max = this.frames.length;
            var idx = Math.floor(this._index);
            frame = this.frames[idx % max];
            if (this.once && idx >= max) {
              this.done = true;
              return;
            }
          } else {
            frame = this._frame;
          }

          var x = this.pos[0];
          var y = this.pos[1];
          var w = this.size[0];
          var h = this.size[1];
 
          x += frame * this.size[0];
          
          ctx.drawImage(resources.get(this.url),
                        x, y, this.size[0], this.size[1],
                        -w / 2, -h / 2, this.size[0], this.size[1]);
          ctx.beginPath();
          ctx.strokeStyle = "white";
          //ctx.arc (x, y, this.size[0]/2, 0, 6.28 )
          ctx.arc (w - this.size[0], h - this.size[1], this.size[0]/2, 0, 6.28 )
          ctx.rect(-w / 2, -h / 2, w, h);
          ctx.stroke();
        