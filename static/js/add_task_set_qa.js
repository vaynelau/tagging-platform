var choiceIndex = 3;
var questionIndex = 2;


function setQuestion() {
    var div = '<div class="form-group" id="question">' +
        '<label for="id_q" id="ques">' +
        '问题' + questionIndex + ':' +
        '</label>' +
        '<input type="text" name="q" class="form-control" maxlength="128" required id="id_q">' +
        '</div>'
    return div;
}


function addQuestion() {
    $("#form-div").append(setQuestion());
    $("#question").attr('id','question'+questionIndex);
    $("#ques").attr('for','id_q'+questionIndex);
    $("#ques").attr('id','ques'+questionIndex);
    $("#id_q").attr('name','q'+questionIndex);
    $("#id_q").attr('id','id_q'+questionIndex);
    questionIndex++;
}

function removeQuestion() {
    questionIndex--;
    $("#question"+questionIndex).remove();
}

function setChoice() {
    var div = '<div class="form-group" id="choice">' +
        '<label for="id_a_q" id="choi">' +
        '选项' + choiceIndex + ':' +
        '</label>' +
        '<input type="text" name="a_q" class="form-control" maxlength="128" required id="id_a_q">' +
        '</div>'
    return div;
}

function addChoice() {
    $("#form-div").append(setChoice());
    $("#choice").attr('id','choice'+choiceIndex);
    $("#choi").attr('for','id_a'+choiceIndex+'_q1');
    $("#choi").attr('id','choi'+choiceIndex);
    $("#id_a_q").attr('name','a'+choiceIndex+"_q1");
    $("#id_a_q").attr('id','id_a'+choiceIndex+"_q1");
    choiceIndex++;
}

function removeChoice() {
    choiceIndex--;
    $("#choice"+choiceIndex).remove();
}