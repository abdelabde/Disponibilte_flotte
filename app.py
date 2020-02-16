import pandas as pd
import tempfile
from flask import Flask, render_template,url_for, request, flash, redirect,make_response, send_file
import pyodbc

# Initialize the Flask application
app = Flask(__name__)
database = 'AfriDispatch3' 
userserver = 'AVORIAZ\SMDC'
username= 'Dispatsh' 
password = 'Dispatsh2019' 
connection = ('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+userserver+';DATABASE='+database+';UID='+username+';PWD='+ password)
try:
    conn=pyodbc.connect(connection)
    print ('connection satified successfully')
except pyodbc.Error :
    print('pyodbc.Error')
mycursor=conn.cursor()
mycursor.fast_executemany = True
@app.route('/')
def form():
    return """
        <html>
            <body>
                <h1 style="position: absolute;top:5%;left:32%;">Disponibilité Des Camions Fioul</h1>
                <div style="background-color:lightgrey;width: 400px;border: 15px solid navy;padding:50px;margin:20px;position: absolute;top:20%;left:28%;">
                <form action="/main_program" method="post" enctype="multipart/form-data">
                    <h3 style="font-style: italic;text-align:center;"> Veuillez entrer les matricules des camions disponibles: </h3>
                    <br>
                    <br>
                      <select name="parking">
                        <option value="HTT">HTT</option>
                        <option value="MEDIA">MEDIA</option>
                        <option value="ParcMazoute">ParcMazoute</option>
                        <option value="PortMEDIA">PortMEDIA</option>
                      </select>
                    <br>
                    <br>
                    <input type="file" name="input_file"  size="60" >
                    <br>
                    <br>
                    <input type="submit" />
                  </form>
                <div/>
                <div  style="position: fixed;top:34%;left:0% ">
                <img src="/static/img/a.png" /height="200" width="350">
                <div/>
                 <div  style="position: fixed;top:34%;left:70%">
                <img src="/static/img/b.png" /height="200" width="350">
                <div/>
            </body>
        </html>
    """

@app.route('/main_program', methods=["POST"])
def main_program_view():
    # Input file
    file = request.files['input_file']
    if not file:
        return "No file"
    tempfile_path = tempfile.NamedTemporaryFile().name
    file.save(tempfile_path)
    data= pd.read_csv(tempfile_path)
    Matricule=list(data['Matricule'])
    Matricule=tuple(Matricule)
    try:
        parking=request.form['parking']
        #Matricule=request.form['Matricule']
        #Matricule=Matricule.split(',')
        #matricule=tuple(Matricule)
        #matricule=ast.literal_eval(Matricule)
        Mat= ', '.join(['?']*len(Matricule))
        sql1 = """update CamionsPN set disponibilite = 'N' where matricule in(select distinct Matricule from CamionsPN)
                update CamionsPN set disponibilite = 'O' where matricule in (%s) """% Mat
        mycursor.execute(sql1,Matricule)
        conn.commit()
        sql2= """update CamionsPN set parking=? where Disponibilite='O'"""
        mycursor.execute(sql2,parking)
        conn.commit()
    #return redirect('/Traitement')
    except Exception as e:
        print(e)
    var=pd.read_sql("""select count(*) from CamionsPN where Disponibilite='O'""",conn)
    return """
        <html>
            <body>
            <div style="background-color:lightgrey;width: 500px;border: 15px solid navy;padding:50px;margin:20px;position: absolute;top:20%;left:28%;">
                <h2 style="font-style: italic;text-align:center;"> La disponibilité des camions Fioul  est inserée</h1>
                <h3 style="text-align:center;border:1px solid blue  width: 10em;"> {var} camions disponibles</h3>
                <img src="/static/img/a.png" /height="100" width="200" style="display: block;margin-left: auto;margin-right: auto;">
                <br>
                <br>
                 <a href="/retour"><input type="button" value="Retour" style="margin:0 auto;display:block; width: 10em;  height: 2em; color: blue;"></a>
            <div/>
         
            </body>
        </html>
    """.format(var=var)
@app.route('/retour')
def retour():
    return """
        <html>
            <body>
                <h1 style="position: absolute;top:5%;left:32%;">Disponibilité Des Camions Fioul</h1>
                <div style="background-color:lightgrey;width: 400px;border: 15px solid navy;padding:50px;margin:20px;position: absolute;top:20%;left:28%;">
                <form action="/main_program" method="post" enctype="multipart/form-data">
                    <h3 style="font-style: italic;text-align:center;"> Veuillez entrer les matricules des camions disponibles: </h3>
                    <br>
                    <br>
                      <select name="parking">
                        <option value="HTT">HTT</option>
                        <option value="MEDIA">MEDIA</option>
                        <option value="ParcMazoute">ParcMazoute</option>
                        <option value="PortMEDIA">PortMEDIA</option>
                      </select>
                    <br>
                    <br>
                    <input type="file" name="input_file"  size="60" >
                    <br>
                    <br>
                    <input type="submit" />
                  </form>
                <div/>
                <div  style="position: fixed;top:34%;left:0% ">
                <img src="/static/img/a.png" /height="200" width="350">
                <div/>
                 <div  style="position: fixed;top:34%;left:70%">
                <img src="/static/img/b.png" /height="200" width="350">
                <div/>
            </body>
        </html>
    """
    
    

    
if __name__ == '__main__':
	#print jdata
  app.run(debug=True)