
// Selections

function fill_select(select_id, element_list) {
    for(i = 0; i < element_list.length; i++) {
        var new_selection = "<option>" + element_list[i] + "</option>";
        document.getElementById(select_id).innerHTML += new_selection;
    }
}

function trigger_onload_select() {
    var id = "Ia_table";
    var element_list = json_data_field['options'][id];
    fill_select(id, element_list);
    index = json_data_field['selections'][id];
    document.getElementById(id).value = element_list[index];

    var id = "cc_table";
    var element_list = json_data_field['options'][id];
    fill_select(id, element_list);
    index = json_data_field['selections'][id];
    document.getElementById(id).value = element_list[index];

    var id = "cc_mass_range";
    var element_list = json_data_field['options'][id];
    fill_select(id, element_list);
    index = json_data_field['selections'][id];
    document.getElementById(id).value = element_list[index];

    var id = "cc_imf";
    var element_list = json_data_field['options'][id];
    fill_select(id, element_list);
    index = json_data_field['selections'][id];
    document.getElementById(id).value = element_list[index];

    var id = "solar_table";
    var element_list = json_data_field['options'][id];
    fill_select(id, element_list);
    index = json_data_field['selections'][id];
    document.getElementById(id).value = element_list[index];

    var id = "ref_element";
    var element_list = json_data_field['options'][id];
    fill_select(id, element_list);
    index = json_data_field['selections'][id];
    document.getElementById(id).value = element_list[index];

    var id = "sigma";
    var element_list = json_data_field['options'][id];
    fill_select(id, element_list);
    index = json_data_field['selections'][id];
    document.getElementById(id).value = element_list[index];
}


// Selections (change)

document.getElementById('Ia_table')
        .addEventListener("change", function(){
            text = $(this).val();
            index = json_data_field['options']['Ia_table'].indexOf(text);
            json_data_field['selections']['Ia_table'] = index;
        });

document.getElementById('cc_table')
        .addEventListener("change", function(){
            text = $(this).val();
            index = json_data_field['options']['cc_table'].indexOf(text);
            json_data_field['selections']['cc_table'] = index;
        });

document.getElementById('cc_mass_range')
        .addEventListener("change", function(){
            text = $(this).val();
            index = json_data_field['options']['cc_mass_range'].indexOf(text);
            json_data_field['selections']['cc_mass_range'] = index;
        });

document.getElementById('cc_imf')
        .addEventListener("change", function(){
            text = $(this).val();
            index = json_data_field['options']['cc_imf'].indexOf(text);
            json_data_field['selections']['cc_imf'] = index;
        });

document.getElementById('solar_table')
        .addEventListener("change", function(){
            text = $(this).val();
            index = json_data_field['options']['solar_table'].indexOf(text);
            json_data_field['selections']['solar_table'] = index;
        });

document.getElementById('ref_element')
        .addEventListener("change", function(){
            text = $(this).val();
            index = json_data_field['options']['ref_element'].indexOf(text);
            json_data_field['selections']['ref_element'] = index;
        });

document.getElementById('sigma')
        .addEventListener("change", function(){
            text = $(this).val();
            index = json_data_field['options']['sigma'].indexOf(text);
            json_data_field['selections']['sigma'] = index;
        });



/*
$(document).ready(function() {
    $('#Ia_table').change(function() {
        text = $(this).val();
        index = json_data_field['options']['Ia_table'].indexOf(text);
        json_data_field['selections']['Ia_table'] = index;
    });

    $('#cc_table').change(function() {
        text = $(this).val();
        index = json_data_field['options']['cc_table'].indexOf(text);
        json_data_field['selections']['cc_table'] = index;
    });

    $('#cc_mass_range').change(function() {
        text = $(this).val();
        index = json_data_field['options']['cc_mass_range'].indexOf(text);
        json_data_field['selections']['cc_mass_range'] = index;
    });

    $('#cc_imf').change(function() {
        text = $(this).val();
        index = json_data_field['options']['cc_imf'].indexOf(text);
        json_data_field['selections']['cc_imf'] = index;
    });

    $('#solar_table').change(function() {
        text = $(this).val();
        index = json_data_field['options']['solar_table'].indexOf(text);
        json_data_field['selections']['solar_table'] = index;
    });

    $('#ref_element').change(function() {
        text = $(this).val();
        index = json_data_field['options']['ref_element'].indexOf(text);
        json_data_field['selections']['ref_element'] = index;
    });

    $('#sigma').change(function() {
        text = $(this).val();
        index = json_data_field['options']['sigma'].indexOf(text);
        json_data_field['selections']['sigma'] = index;
    });
});
*/



// Load Data
/*
document.getElementById('load_data')
        .addEventListener('change', getFile)

function getFile(event) {
    const input = event.target
    if ('files' in input && input.files.length > 0) {
    placeFileContent(
        document.getElementById('content-target'),
        input.files[0])
    }
}

function placeFileContent(target, file) {
    readFileContent(file).then(content => {
    target.value = content
    }).catch(error => console.log(error))
}

function readFileContent(file) {
    const reader = new FileReader()
    return new Promise((resolve, reject) => {
    reader.onload = event => resolve(event.target.result)
    reader.onerror = error => reject(error)
    reader.readAsText(file)
    })
}
*/



// Fit

$(document).ready(function() {
    $('#btn_fit').click(function() {

      $("#status").value = "Fitting..";

      all_elements = ['C', 'N', 'O', 'Ne', 'Mg', 'Al', 'Si', 'S', 'Ar', 'Ca', 'Fe', 'Ni'];
      selected_elements = []
      abund = []
      abund_err = []

      if($('#chb_C').prop("checked") == true) {
          selected_elements.push('C');
          abund.push($('#val_C').val());
          abund_err.push($('#err_C').val());
        }
      
      if($('#chb_N').prop("checked") == true) {
        selected_elements.push('N');
        abund.push($('#val_N').val());
        abund_err.push($('#err_N').val());
      }

      if($('#chb_O').prop("checked") == true) {
        selected_elements.push('O');
        abund.push($('#val_O').val());
        abund_err.push($('#err_O').val());
      }

      if($('#chb_Ne').prop("checked") == true) {
        selected_elements.push('Ne');
        abund.push($('#val_Ne').val());
        abund_err.push($('#err_Ne').val());
      }

      if($('#chb_Mg').prop("checked") == true) {
        selected_elements.push('Mg');
        abund.push($('#val_Mg').val());
        abund_err.push($('#err_Mg').val());
      }

      if($('#chb_Al').prop("checked") == true) {
        selected_elements.push('Al');
        abund.push($('#val_Al').val());
        abund_err.push($('#err_Al').val());
      }

      if($('#chb_Si').prop("checked") == true) {
          selected_elements.push('Si');
          abund.push($('#val_Si').val());
          abund_err.push($('#err_Si').val());
        }
      
      if($('#chb_S').prop("checked") == true) {
        selected_elements.push('S');
        abund.push($('#val_S').val());
        abund_err.push($('#err_S').val());
      }

      if($('#chb_Ar').prop("checked") == true) {
        selected_elements.push('Ar');
        abund.push($('#val_Ar').val());
        abund_err.push($('#err_Ar').val());
      }

      if($('#chb_Ca').prop("checked") == true) {
        selected_elements.push('Ca');
        abund.push($('#val_Ca').val());
        abund_err.push($('#err_Ca').val());
      }

      if($('#chb_Fe').prop("checked") == true) {
        selected_elements.push('Fe');
        abund.push($('#val_Fe').val());
        abund_err.push($('#err_Fe').val());
      }

      if($('#chb_Ni').prop("checked") == true) {
        selected_elements.push('Ni');
        abund.push($('#val_Ni').val());
        abund_err.push($('#err_Ni').val());
      }

      json_data_field['elements']['element'] = selected_elements;
      json_data_field['elements']['abund'] = abund;
      json_data_field['elements']['abund_err'] = abund_err;

      json_data_field['results']['fit_results'] = '';

      $('#hidden_val').prop("value", JSON.stringify(json_data_field));
        
      $('#fit_image').prop("src", "data:image/png;base64,{{ img_data | safe }}");

    });
});



// Fit All

$(document).ready(function() {
    $('#btn_fit_loop').click(function() {

      $("#status").value = "Fitting for all models..";

      all_elements = ['C', 'N', 'O', 'Ne', 'Mg', 'Al', 'Si', 'S', 'Ar', 'Ca', 'Fe', 'Ni'];
      selected_elements = []
      abund = []
      abund_err = []

      if($('#chb_C').prop("checked") == true) {
          selected_elements.push('C');
          abund.push($('#val_C').val());
          abund_err.push($('#err_C').val());
        }
      
      if($('#chb_N').prop("checked") == true) {
        selected_elements.push('N');
        abund.push($('#val_N').val());
        abund_err.push($('#err_N').val());
      }

      if($('#chb_O').prop("checked") == true) {
        selected_elements.push('O');
        abund.push($('#val_O').val());
        abund_err.push($('#err_O').val());
      }

      if($('#chb_Ne').prop("checked") == true) {
        selected_elements.push('Ne');
        abund.push($('#val_Ne').val());
        abund_err.push($('#err_Ne').val());
      }

      if($('#chb_Mg').prop("checked") == true) {
        selected_elements.push('Mg');
        abund.push($('#val_Mg').val());
        abund_err.push($('#err_Mg').val());
      }

      if($('#chb_Al').prop("checked") == true) {
        selected_elements.push('Al');
        abund.push($('#val_Al').val());
        abund_err.push($('#err_Al').val());
      }

      if($('#chb_Si').prop("checked") == true) {
          selected_elements.push('Si');
          abund.push($('#val_Si').val());
          abund_err.push($('#err_Si').val());
        }
      
      if($('#chb_S').prop("checked") == true) {
        selected_elements.push('S');
        abund.push($('#val_S').val());
        abund_err.push($('#err_S').val());
      }

      if($('#chb_Ar').prop("checked") == true) {
        selected_elements.push('Ar');
        abund.push($('#val_Ar').val());
        abund_err.push($('#err_Ar').val());
      }

      if($('#chb_Ca').prop("checked") == true) {
        selected_elements.push('Ca');
        abund.push($('#val_Ca').val());
        abund_err.push($('#err_Ca').val());
      }

      if($('#chb_Fe').prop("checked") == true) {
        selected_elements.push('Fe');
        abund.push($('#val_Fe').val());
        abund_err.push($('#err_Fe').val());
      }

      if($('#chb_Ni').prop("checked") == true) {
        selected_elements.push('Ni');
        abund.push($('#val_Ni').val());
        abund_err.push($('#err_Ni').val());
      }

      json_data_field['elements']['element'] = selected_elements;
      json_data_field['elements']['abund'] = abund;
      json_data_field['elements']['abund_err'] = abund_err;

      json_data_field['results']['fit_results'] = '';


      $('#hidden_val_loop').prop("value", JSON.stringify(json_data_field));
      
      $('#fit_image').prop("src", "data:image/png;base64,{{ img_data | safe }}");

    });
});


/*
function myLoop() {
  var done = false;
  while(!done) {
    if(!json_data_field['fit_loop_result']) {

      var intervalId = window.setInterval(function(){
        document.getElementById("val_chi").value += "*";
      }, 100);
            
      //clearInterval(intervalId) 
      
    }
  }
}
*/

var in_loop = false;
var intervalId = null;
var percent = "0";

document.getElementById('btn_loop_trigger')
.addEventListener("click", function(){

  if(in_loop == false) {

    in_loop = true;

    intervalId = window.setInterval(function(){
      document.getElementById("my_p").innerHTML += "*";
  
      //document.getElementById("btn_fit_loop").click();
      /*
      document.getElementsByName("fit_loop").submit();
      in_loop = json_data_field["results"]["fit_loop_status"];
      percent = json_data_field["results"]["fit_loop_progress_percent"];

      if(in_loop == false) {
        clearInterval(intervalId);
      }
      */

    }, 500);

  } else {

    in_loop = false;

    clearInterval(intervalId);

  }
     
  //clearInterval(intervalId) 

});

// Load File

document.getElementById('load_data').onchange = function(){

    var file = this.files[0];
  
    var reader = new FileReader();
    reader.onload = function(progressEvent){
      // Entire file
      //console.log(this.result);
      //document.getElementById('content-target').value = this.result;

     // $(':checkbox').prop('checked', 'false');

  
      // By lines
      var lines = this.result.split('\n');

      var element_list = [];
      var val_list = [];
      var err_list = [];

      for(var i = 1; i < lines.length; i++){
        //console.log(lines[line]);
        //document.getElementById('content-target').value += lines[i] + '\n';
        ele = lines[i].split(' ')[0];
        val = lines[i].split(' ')[1];
        err = lines[i].split(' ')[2];

        document.getElementById('chb_' + ele).checked = true;

        document.getElementById('val_' + ele).value = val;
        document.getElementById('val_' + ele).disabled = false;

        document.getElementById('err_' + ele).value = err;
        document.getElementById('err_' + ele).disabled = false;

      }
    };
    reader.readAsText(file);
};



// Reset Elements
// doesn't work!!
/*
$('#btn_reset').click(function() {
    $(':checkbox').prop('checked', false);
    $('.form-control').prop('value', '');
    $('.form-control').prop('disabled', true);
});
*/

// Detailed Results

document.getElementById('btn_detailed_results')
        .addEventListener("click", function(){
            alert(json_data_field["results"]["fit_results_text"])
        });



// onload events
function trigger_onload() {
    trigger_onload_select();
}

window.onload = trigger_onload;
