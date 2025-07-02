# 🌐 LG Ultra – Looking Glass Web Interface

**LG Ultra** é uma aplicação web feita com Django que permite visualizar rotas BGP e caminhos AS_PATH de forma interativa e visual.  
Ideal para operadoras, IXPs e engenheiros de rede que desejam observar como seus prefixos estão sendo anunciados na internet.

> ⚠️ **Atenção**: Para melhor desempenho e cobertura de rotas, recomenda-se o uso de conexões com suporte a **IPv6**.

> ⚠️ **Note**: For better performance and full route visibility, it is recommended to access the service over an **IPv6-enabled connection**.

---

## 🚀 Instalação

```bash
git clone https://github.com/GabrielMend/LG_ULTRA.git
cd LG_ULTRA
docker-compose up -d
```

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


## 🌐 LG Ultra - Looking Glass Web Interface (English)

**LG Ultra** is a web application built with Django that allows interactive and visual inspection of BGP routes and AS_PATH information. Ideal for ISPs, IXPs, and network engineers who want to understand how their prefixes are being advertised across the Internet.

### ✨ Features

- 🔎 BGP Lookup with IP or prefix input  
- 🧮 Automatic AS_PATH analysis (last, penultimate, and antepenultimate AS)  
- 🧠 Detection of **Tier 1** AS presence  
- 📊 Dynamic charts using **Chart.js**  
- 🎨 Modern UI with **Bootstrap 5**  
- 🌙 Dark/light mode with persistent theme  
- 🇧🇷 Portuguese user interface  

### 📸 Screenshots

| Dark Theme | Light Theme |
|------------|-------------|
| ![Dark](https://raw.githubusercontent.com/GabrielMend/LG_ULTRA/main/assets/black.png) | ![Light](https://raw.githubusercontent.com/GabrielMend/LG_ULTRA/main/assets/light.png) |

### ⚙️ Tech Stack

- [Python 3.11+](https://www.python.org)
- [Django 5+](https://www.djangoproject.com/)
- [Bootstrap 5](https://getbootstrap.com)
- [Chart.js](https://www.chartjs.org/)
- [Bootstrap Icons](https://icons.getbootstrap.com)





