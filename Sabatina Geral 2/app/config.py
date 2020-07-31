class Config:

  SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Users/Mr. Egg/Desktop/Area de Trabalho/1.UFRJ/Fluxo/Processo seletivo/Trainee/Projetos/Flask 5/data.sqlite'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  JSON_SORT_KEYS = False

  MAIL_SERVER = 'smtp.sendgrid.net'
  MAIL_PORT = 587 
  MAIL_USERNAME = 'apikey'
  MAIL_PASSWORD = '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'
  MAIL_USER_TLS = True
  MAIL_USE_SSL = False

  JWT_SECRET_KEY = 'segredo'