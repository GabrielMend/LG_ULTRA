# 🌐 LG Ultra - Looking Glass Web Interface

LG Ultra é uma aplicação web feita com Django que permite visualizar rotas BGP e caminhos AS_PATH de forma interativa e visual. Ideal para operadoras, IXPs e engenheiros de rede que desejam observar como seus prefixos estão sendo anunciados na internet.

## ✨ Funcionalidades

- 🔎 Consulta BGP (Looking Glass) com IP ou prefixo
- 🧮 Análise automática de AS_PATH (último, penúltimo, antepenúltimo AS)
- 🧠 Detecção de presença de **Tier 1** no caminho
- 📊 Gráficos dinâmicos com **Chart.js**
- 🎨 Interface moderna com **Bootstrap 5**
- 🌙 Modo escuro/claro com persistência
- 🇧🇷 Interface em português

## 📸 Capturas de Tela

| Tema Escuro | Tema Claro |
|------------|-------------|
| ![Claro](https://raw.githubusercontent.com/GabrielMend/LG_ULTRA/main/assets/light.png) | ![Escuro](https://raw.githubusercontent.com/GabrielMend/LG_ULTRA/main/assets/black.png) |


## ⚙️ Tecnologias Utilizadas

- [Python 3.11+](https://www.python.org)
- [Django 5+](https://www.djangoproject.com/)
- [Bootstrap 5](https://getbootstrap.com)
- [Chart.js](https://www.chartjs.org/)
- [Bootstrap Icons](https://icons.getbootstrap.com)

## 🚀 Instalação

```bash
git clone https://github.com/GabrielMend/LG_ULTRA.git
cd LG_ULTRA
python -m venv venv
venv\Scripts\activate   # No Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


Em breve Dockerfile e também a aplicação na AWS 
