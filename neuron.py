class Neuron(object):
  a =  0.02
  b = -0.04

  def __learn(self,D):
    """
    Обучение
    """
    w = self.w[:]
    f = self.__call__
    for d in D: 
      x = d[0] 
      y = d[1] 
      for j in range(len(x)):
        self.w[j] += self.a * (y - f(x)) * x[j]
    return w != self.w 

  def __sigma_s(self,x):
    return x

  def __sigma_l(self,x):
    if x < 0:
      return 0
    if x >= 0 and x <= 1:
      return x
    if x > 1:
      return 1
    
  def __sigma_p(self,x):
    if x > 0:
      return 1
    else:
      return 0

  def __call__(self,x):
    sigma = self.__sigma_s
    s = self.b
    for i in range(len(x)):
      s += self.w[i] * x[i]
    # w = self.w[:]
    # s += (w[0]*x[0]**2 + w[1]*x[1]**2) * (w[4]*(x[0]-w[2])**2 + w[5]*(x[1]-w[3])**2)
    return sigma(s)

  def __init__(self,D):
    """
    Создание и обучение
    """
    self.w = [0]*len(D[0][0]) 
    self.c = 0
    while self.__learn(D):
      self.c += 1
      if self.c > 10000: return None

