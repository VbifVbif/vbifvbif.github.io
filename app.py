from flask import Flask, render_template, request, render_template_string

app = Flask(__name__)

HTML = '''
   <!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Risk Assessment App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
  </head>
  <body class="p-3 mb-2 bg-danger.bg-gradient text-emphasis-primary">
    <h1 ></h1>

    <div class="container-sm mx-auto d-block content">
       <div class="row shadow-lg p-3 mb-5 bg-body-tertiary rounded" >

        <div class="col-md-3 shadow-lg p-3 mb-5 bg-body-tertiary rounded">
           <form id="dataForm" action="/" method="post">
                <input class="form-control" list="datalistOptions" id="exampleDataList" placeholder="Enter CIA values (3, 4, 2)" required type="text" id="cia" name="cia">
                <input class="form-control" list="datalistOptions" id="exampleDataList" placeholder="Enter weights (0.5, 0.3, 0.2)" required type="text" id="weights" name="weights">
                <input class="form-control" list="datalistOptions" id="exampleDataList" placeholder="Enter susceptibility value (0.8)" required type="text" id="susceptibility" name="susceptibility">
                <input class="form-control" list="datalistOptions" id="exampleDataList" placeholder="Enter exposure value (0.6)" required type="text" id="exposure" name="exposure">
                <button type="submit" class="btn btn-success btn-lg shadow-lg">Calculate</button>
          </form>
        </div>
        <div class="col-md-2"></div>
        <div class="col-md-6" > 
          
                <table class="table align-middle col-md-3 shadow-lg p-3 mb-5 bg-body-tertiary rounded">

  <tbody >
    <tr>
      <th scope="row">Risk Impact:</th>
      <td> {% if result %} {{ result }}  {% endif %}</td>


    </tr>
    <tr>
      <th scope="row">Impact Assessment:</th>
      <td> {% if result %} {{ result1 }}  {% endif %}</td>


    </tr>
    <tr>
      <th scope="row">Probability of Threat Occurrence: </th>
      <td>{% if result %} {{ result2 }}  {% endif %} </td>
    </tr>
    <tr>
      <th scope="row">Rank Threat: </th>
      <td>{% if result %} {{ result3 }}  {% endif %} </td>
    </tr>
  </tbody>
</table>

        </div>
        
        
    </div>
  </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js" integrity="sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.min.js" integrity="sha384-BBtl+eGJRgqQAUMxJ7pMwbEyER4l1g+O15P+16Ep7Q9Q+zqX6gSbd85u4mG4QzX+" crossorigin="anonymous"></script>
  </body>
  <style>
    input{
      margin-top: 20px;
    }
    button{
      margin-top: 20px;
    }
    .content{
      margin-top: 40px;
    }
    
    </style>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script>

</script>
</html>
'''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def calculate():
    cia_values = list(map(float, request.form.get('cia').split(',')))
    weights = list(map(float, request.form.get('weights').split(',')))
    susceptibility = float(request.form.get('susceptibility'))
    exposure = float(request.form.get('exposure'))

    #Input
    if len(cia_values) != 3 or len(weights) != 3 or not all(isinstance(val, (int, float)) for val in cia_values + weights) or \
       not isinstance(susceptibility, (int, float)) or not isinstance(exposure, (int, float)):
        return 'Invalid input. Please enter valid values.'

    #Calculate Risk Impact
    risk_impact = sum(c * w for c, w in zip(cia_values, weights))

    #Calculate Impact Assessment
    impact_assessment = risk_impact * susceptibility * exposure

    #Calculate Probability of Threat Occurrence
    probability = risk_impact * exposure

    #Rank Threat
    rank = impact_assessment * probability

    #Result
    result = f'Risk Impact: {risk_impact:.2f}<br>' \
                  f'Impact Assessment: {impact_assessment:.2f}<br>' \
                  f'Probability of Threat Occurrence: {probability:.2f}<br>' \
                  f'Rank Threat: {rank:.2f}'

    return render_template_string(HTML, result=round(risk_impact, 1), result1=round(impact_assessment, 1), result2=round(probability, 1), result3=round(rank, 1))

if __name__ == '__main__':
    app.run(debug=True)
