var questionIndex = 2;
var choiceIndex = new Array();

choiceIndex[0]=3;


function setQuestion() {
    var div = '<div id="form-divv" class="col-md-12" style="margin-bottom: 40px;">' +
        '<div class="form-group">' +
        '<label for="id_q" id="ques">' +
        '问题'+questionIndex+':' +
        '</label>' +
        '<input type="text" name="q" class="form-control" maxlength="128" required id="id_q" />' +
        '</div>' +
        '<div class="form-group">' +
        '<label for="id_a1_q" id="choi1">选项1:</label>' +
        '<input type="text" name="a1_q" class="form-control" maxlength="128" required id="id_a1_q" />' +
        '</div>' +
        '<div class="form-group">' +
        '<label for="id_a2_q" id="choi2">选项2:</label>' +
        '<input type="text" name="a2_q" class="form-control" maxlength="128" required id="id_a2_q" />' +
        '</div>' +
        '<div class="col-md-8" style="top:-120px;left:300px;margin-bottom: -800px;">' +
        '<img class="a" src="../static/css/queding.png/" width="35px" height="35px" onclick="addChoice(this)" id="add"/>' +
        '<span width="40px;" height="40px;" style="font-size: 18px;">增加选项</span>' +
        '</div>' +
        '<div class="col-md-8" style="top:-80px;left:300px;margin-bottom: -800px;">' +
        '<img class="a" src="../static/css/shanchuxuanxiang.png/" width="35px" height="35px" onclick="removeChoice(this)" id="del"/>' +
        '<span width="40px;" height="40px;" style="font-size: 18px;">删除选项</span>' +
        '</div>' +
        '</div>';
    return div;
}


function addQuestion() {
    $("#addform").prepend(setQuestion());
    $("#form-divv").attr('id','form-div'+questionIndex);
    $("#question").attr('id','question'+questionIndex);
    $("#ques").attr('for','id_q'+questionIndex);
    $("#ques").attr('id','ques'+questionIndex);
    $("#id_q").attr('name','q'+questionIndex);
    $("#id_q").attr('id','id_q'+questionIndex);
    $("#choi1").attr('for','id_a1_q'+questionIndex);
    $("#choi2").attr('for','id_a1_q'+questionIndex);
    $("#id_a1_q").attr('name','a1_q'+questionIndex);
    $("#id_a1_q").attr('id','id_a1_q'+questionIndex);
    $("#id_a2_q").attr('name','a2_q'+questionIndex);
    $("#id_a2_q").attr('id','id_a2_q'+questionIndex);
    $("#add").attr('id','add'+questionIndex);
    $("#del").attr('id','del'+questionIndex);
    choiceIndex[questionIndex-1] = 3;
    questionIndex++;
}

function removeQuestion() {
    questionIndex--;
    choiceIndex[questionIndex-1] = 3;
    $("#form-div"+questionIndex).remove();
}

function setChoice() {
    var div = '<div class="form-group" id="choice">' +
        '<label for="id_a_q" id="choi">' +
        '</label>' +
        '<input type="text" name="a_q" class="form-control" maxlength="128" required id="id_a_q">' +
        '</div>'
    return div;
}

function addChoice(t) {
    $(t).parents('.col-md-12').append(setChoice());
    var index = $(t).attr('id').substr($(t).attr('id').length-1,1);
    $("#choice").attr('id','choice'+choiceIndex[index-1]);
    $("#choi").attr('for','id_a'+choiceIndex[index-1]+"_q"+index);
    $("#choi").html("选项"+choiceIndex[index-1]);
    $("#choi").attr('id','choi'+choiceIndex[index-1]);
    $("#id_a_q").attr('name','a'+choiceIndex[index-1]+"_q"+index);
    $("#id_a_q").attr('id','id_a'+choiceIndex[index-1]+"_q"+index);
    choiceIndex[index-1]++;
}

function removeChoice(t) {
    var index = $(t).attr('id').substr($(t).attr('id').length-1,1);
    choiceIndex[index-1]--;
    $(t).parents('.col-md-12').find('#choice'+choiceIndex[index-1]).remove();
}