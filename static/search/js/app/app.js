var app = new function() {

  _app = this;
  this.els = {}
  this.data = {};
  this.elSelectors = {
    'searchUsername': '.serach__username',
    'searchPage': '.serach__page',
    'serachError': '.serach__error',
    'serachBtn': '.serach__btn',
    'dataTable': '#data--table',
    'datePicker': '.navbar .input-daterange',
    'startDate': '.serach__startDate', 
    'endDate': '.serach__endDate'
  }
  this.elEvents = {
    'click .serach__btn' : 'requestData'
  }


  this.selectUI = function() {
    $.each(this.elSelectors, function(i, selector) {
      app.els[i] = $(selector);
    });
  }

  this.addEvents = function() {
    $.each(this.elEvents, function(ev, fn) {
      var _event = ev.split(' ')[0];
      var _el = ev.split(' ')[1];

      $(_el)[_event](function() {
        app[fn]();
      })
    })
  }

  this.getSearchParams = function() {
    var params = {
      'type': 'error-scarer'
    };

    params['user_id'] = $(this.els.searchUsername).val();
    params['page'] = $(this.els.searchPage).val();
    params['message'] = $(this.els.serachError).val();
    params['since'] = $(this.els.startDate).val();
    params['until'] = $(this.els.endDate).val();

    return params;
  }

  this.requestData = function() {
    params = this.getSearchParams();
    console.log('params', params);

    $.ajax({
      url: 'http://error_scarer-dev.buzzfeed.com/logs',
      data: params
    })
    .done(function(r) {
      console.log('r', r);
      if (r && r.logs) {
        app.showResults(r.logs);
      }
    })
  }

  this.showResults = function(data) {
    console.log('-------', data);
    console.log('this.els.dataTable', this.els.dataTable);
    this.els.dataTable.bootstrapTable({
      data: data
    });
  }

  this.addDatePicker = function() {
    $(this.els.datePicker).datepicker({
      format: "yyyy/dd/mm"
    });
  }

  this.init = function() {
    this.selectUI();
    this.addEvents();
    this.addDatePicker();
    this.requestData();
  }

}

$(document).ready(function() {
  app.init();
})
