<!doctype html>

<html lang="en">
<head>
    <meta charset="utf-8">

    <title>Ruby Light Manager</title>
    <meta name="description" content="Ruby Light Manager">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <link rel="stylesheet" href="css/toastr.css?v=1.0">
    <link rel="stylesheet" href="css/styles.css?v=1.0">

    <!-- Optional theme -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

    <!--[if lt IE 9]>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7.3/html5shiv.js"></script>
    <![endif]-->
    <style>
        .color-circle {
            height: 20px;
            width: 20px;
            border: 1px solid #333;
            border-radius: 16px;
            display: inline-block;

            transition: all .2s ease-in-out;
        }
        .color-circle:hover {
            transform: scale(1.1);
        }
    </style>
</head>

<body>
    <nav class="navbar navbar-inverse navbar-fixed-top">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="#">Ruby Light Manager</a>
            </div>
            <div id="navbar" class="collapse navbar-collapse">
                <ul class="nav navbar-nav">
                    <li class="active"><a href="#">Home</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </div><!--/.nav-collapse -->
        </div>
    </nav>

    <div class="container">

        <div class="row">
            <div class="col-md-4">
                <h2>Sequences</h2>
                <select class="sequence-picker">
                    <option value="">Select Sequence</option>
                    % for sequence in sequences:
                    <option value="{{sequence.id}}">{{sequence.name}}</option>
                    % end
                </select>
                <div class="btn btn-default btn-sequence">Show Sequence</div>
            </div>
            <div class="col-md-4">
                <h2>Blackout</h2>
                <div class="btn btn-default btn-blackout">Set</div>

                <h2>Solid</h2>
                <div>Outer Color: <input class="jscolor outer-color-solid" value="ff6961"></div>
                <div>Inner Color: <input class="jscolor inner-color-solid" value="9b111e"></div>
                <div class="btn btn-default btn-solid">Set Color</div>

                <h2>Ombre</h2>
                <div>Outer Color Lower: <input class="jscolor outer-color-solid-lower" value="ff6961"></div>
                <div>Outer Color Upper: <input class="jscolor outer-color-solid-upper" value="ff6961"></div>
                <div>Inner Color Lower: <input class="jscolor inner-color-solid-lower" value="9b111e"></div>
                <div>Inner Color Upper: <input class="jscolor inner-color-solid-upper" value="9b111e"></div>
                <div class="btn btn-default btn-ombre">Set Color</div>
            </div>
            <div class="col-md-4">
                <h2>Quick</h2>
                <div class="quick-color-container">
                    % for color in colors:
                    <span class="color-circle" color="{{color}}" style="background-color:#{{color}}"></span>
                    % end
                </div>
            </div>
        </div>
    </div>
    <!-- /.container -->

    <script src="https://code.jquery.com/jquery-3.2.1.min.js" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" crossorigin="anonymous"></script>

    <script src="./js/underscore-min.js"></script>
    <script src="./js/extend.js"></script>
    <script src="./js/toastr.min.js"></script>
    <script src="./js/my.class.min.js"></script>
    <script src="./js/pinocchio.js"></script>
    <script src="./js/moment.min.js"></script>
    <script src="./js/jscolor.js"></script>
    <script src="./js/scripts.js"></script>
</body>
</html>