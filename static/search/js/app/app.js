var app = new function() {

  _app = this;
  this.els = {}
  this.data = {};
  this.elSelectors = {
    'searchUsername': '.serach__username',
    'searchPage': '.serach__page',
    'serachError': '.serach__error',
    'serachBtn': '.serach__btn',
    'dataTable': '#data--table'
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

    data['username'] = $(this.els.searchUsername).val();
    data['page'] = $(this.els.searchPage).val();
    data['error'] = $(this.els.serachError).val();

    return params;
  }

  this.requestData = function() {
    params = this.getSearchParams();

    $.ajax({
      url: '',
      data: params
    })
    .done(function(r) {
      app.showResults(r);
    })
  }

  this.showResults = function(data) {
    this.els.dataTable.bootstrapTable({
      data: data
    });
  }

  this.init = function() {
    this.selectUI();
    this.addEvents();

    app.showResults(mock_data)
  }

}

$(document).ready(function() {
  app.init();
})
