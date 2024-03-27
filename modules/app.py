import os
import json

from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests


app = Flask(__name__, static_url_path='/static')

# Caminho absoluto do arquivo em execução
caminho_absoluto = os.path.abspath(__file__)

# Diretório do arquivo em execução
root = os.path.dirname(caminho_absoluto)

text_path =  root + '/locate'

#API JAVA
app.api = 'http://localhost:8080/'


@app.before_request
def before_request():
    # Define um idioma padrão se nenhum tiver sido selecionado ainda.
    if 'language' not in session:
        session['language'] = 'pt_BR'
        session['text'] = read_translation(session['language'])
    else:
        session['text'] = read_translation(session['language'])


@app.route('/set_language', methods=['POST'])
def set_language():
    language = request.form.get('language')
    if language:
        session['language'] = language
        # Carregar as traduções para o idioma escolhido e salvar na sessão.
        session['text'] = read_translation(language)
        
    # Redirecionar para a página de onde veio, ou para a página inicial se o referenciador não estiver disponível.
    return redirect(request.referrer or url_for('login_screen'))

# Ler arquivo de internacionalização
def read_translation(language):

    file_path = f'{text_path}/{language}.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        translations = json.load(file)
    return translations

# Rota para a página de login
@app.route('/', methods=['GET','POST'])
def login_screen():

    if request.method == 'POST':
        # Aqui você captura os dados do formulário e envia para a API Java
        email = request.form['email_login']
        senha = request.form['senha_login']
        
        # TODO integração com JAVA via API

        response = requests.post( app.api, json={'email': email, 'senha': senha})

        # Teste
        response.ok = True

        # TODO inserir quantidade de tentativas
        if response.ok:
            # Obter permissões CRUD e enviar POST para admin
            return redirect(url_for('admin_screen'))
        else:
            # Se a API Java responder com erro, retorne à tela de login com uma mensagem de erro
            return render_template('login_screen.html', text=session['text'], error='Login inválido.')
        
    # Se o método for GET, apenas exiba a tela de login.
    return render_template('login_screen.html', text=session['text'])    

# Rota para a página de cadastro
@app.route('/create_account', methods=['GET', 'POST'])
def create_account_screen():
    if request.method == 'POST':
        # Captura os dados do formulário
        user_data = {
            "nome": request.form['nome_cad'],
            "email": request.form['email_cad'],
            "data_nasc": request.form['data_nasc_cad'],
            "cpf": request.form['cpf_cad'],
            "senha": request.form['senha_cad']
        }

        # Envia os dados do usuário para a API
        response = requests.post('http://localhost:8080/create', json=user_data)

        if response.status_code == 201:
            # Usuário criado com sucesso, redirecionar para a tela de login ou outra página
            return redirect(url_for('login_screen'))
        else:
            # Trata erros possíveis
            flash("Erro ao criar usuário: " + response.json().get("mensagem", ""))
             # Se a API Java responder com erro, retorne à tela de login com uma mensagem de erro
            return render_template('login_screen.html', text=session['text'], error='Login inválido.')

    # Se o método for GET ou se o cadastro falhar, mostra a tela de cadastro novamente
    return render_template('create_acc_screen.html', text=session['text'])

# Rota para a página de recuperação de senha
@app.route('/recover_password', methods=['GET', 'POST'])
def recover_password():
    if request.method == 'POST':
        
        email = request.form['email_recovery']
        cpf = request.form['cpf_recovery']
        data_nasc = request.form['data_nasc_recovery']

        # TODO checar na API validade
        response = requests.post(app.api + '/check', json={'email': email,
                                                           'cpf': cpf,
                                                           'data_nasc': data_nasc})
        if response.ok:
            return redirect(url_for('change_password.html'), text=session['text'])
        else:
            return render_template('recover_password.html', text=session['text'], error='Dados inválido.')

    
    return render_template('recover_password.html', text=session['text'])

# Rota para a página de alteração de senha
@app.route('/change_password/<email>', methods=['GET', 'POST'])
def change_password(email):

    if request.method == 'POST':
        # Processar o formulário de alteração de senha
        nova_senha = request.form['nova_senha']
        confirma_senha = request.form['confirma_senha']
        if nova_senha == confirma_senha:
            return redirect(url_for('password_changed', text=session['text'], email=email))
        else:
            # Senhas não coincidem, exibir mensagem de erro
            error_message = "As senhas digitadas não coincidem."
            return render_template('change_password.html', text=session['text'], error_message=error_message, email=email)
    else:
        return render_template('change_password.html', text=session['text'], email=email)

# Rota para a página de sucesso na alteração de senha
@app.route('/password_changed/<email>', methods=['GET', 'POST'])
def password_changed(email):
    return render_template('password_changed.html', text=session['text'], email=email)

# Rota para a página de administração do site
@app.route('/admin_screen', methods=['GET', 'POST'])
def admin_screen():
    # Enviar permissões possíveis
    return render_template('admin_screen.html', text=session['text'])
    
if __name__ == '__main__':
    app.run(debug=True)
    
    