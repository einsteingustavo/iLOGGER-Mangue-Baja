# Manual do Desenvolvedor
Este projeto foi feito utilizando o pacote Tkinter do python, cuja documentação<br/>
pode ser encontrada no link: https://docs.python.org/3/library/tkinter.html<br/><br/>

Notas:<br/>
- O pós processamento foi feito baseado num script anterior que se encontra na<br/>
pasta BACKUP.<br/>
- A tradução de binário para csv foi feita baseada num script em "C" que também se</br>
encontra na pasta BACKUP.<br/>
- A biblioteca de link dinâmico(DLL) utilizada foi compilada no CodeBlocks, sendo<br/> 
o projeto criado a partir da opção "Shared Library". O projeto inteiro se encontra<br/>
na pasta SHARED_LIBRARY.<br/><br/>

Para efetuar alterações e criar o executável novamente:<br/>
- Criar projeto no CodeBlocks com a função de shared library como dito mais acima,<br/>
copiar os arquivos principais para dentro do seu projeto e compilar.<br/>
(dentro da pasta "bin" vai estar o DLL atualizado a cada re-compilação<br/>
caso você deseje atualizar no PyCharm)<br/>
- Criar projeto no PyCharm e copiar pra dentro dele os arquivos pertinentes:<br/>
(main.py, icone.ico, icone_window.png, libshared_read_object.dll),<br/>
efetuar mudanças desejadas no Python (main.py) e testar a GUI.<br/>
- Para gerar um novo executável instalar o PyInstaller e utilizar no terminal o comando:<br/>
pyinstaller --icon=icone.ico -F -w main.py<br/>
Documentação do PyInstaller para melhor entender o comando: https://pyinstaller.org/en/stable/.<br/>
Serão criadas duas novas pastas, o executável estará na pasta "dist", e precisará dos<br/>
arquivos "icone_window.png" e "libshared_read_object.dll" para funcionar devidamente.
