
var textAreaContents = new Array(2);
var elemId;

function outf(text) {
    var mypre = document.getElementById(elemId);
    mypre.innerHTML = mypre.innerHTML + text;
}
function builtinRead(x) {
    if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
        throw "File not found: '" + x + "'";
    return Sk.builtinFiles["files"][x];
}

function runit(elem) {
    elemId = elem;

    var prog;

    if (elem == 'output1'){
        prog = textAreaContents[0].getValue();
    }
    else{
        prog = textAreaContents[1].getValue();
    }

    var mypre = document.getElementById(elemId);
    mypre.innerHTML = '';
    Sk.pre = "output";
    Sk.configure(
        {
            inputfun: function (prompt) {
                return window.prompt(prompt);
            },
            inputfunTakesPrompt: true,
            output: outf,
            read: builtinRead
        });

    (Sk.TurtleGraphics || (Sk.TurtleGraphics = {})).target = 'mycanvas';

    var myPromise = Sk.misceval.asyncToPromise(function () {
        return Sk.importMainWithBody("<stdin>", false, prog, true);
    });

    myPromise.then(function (mod) {
            console.log('success');
        },
        function (err) {
            console.log(err.toString());
            mypre.innerHTML = err.toString();
        });
}

window.onload = function () {

    for (var i = 0; i < 2; ++i) {
        textAreaContents[i] = CodeMirror.fromTextArea(document.getElementsByClassName("code-place")[i], {
            mode: {
                name: "python",
                version: 3,
                singleLineStringErrors: false
            },
            lineNumbers: true,
            indentUnit: 4,
            matchBrackets: true
        });
    }

};

