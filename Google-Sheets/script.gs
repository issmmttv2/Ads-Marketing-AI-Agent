// Tools > Script
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Marketing Dashboard')
    .addItem('Filter Timeline', 'showTimelineFilter')
    .addItem('Sort Client Dashboard', 'sortClientDashboard')
    .addToUi();
}

function showTimelineFilter() {
  var ui = SpreadsheetApp.getUi();
  var result = ui.prompt('Enter Timeline (3, 7, 14, 21, 30, 45, 60 days):', ui.ButtonSet.OK_CANCEL);
  if (result.getSelectedButton() == ui.Button.OK) {
    var days = parseInt(result.getResponseText());
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Dashboard');
    var data = sheet.getDataRange().getValues();
    var filteredData = data.filter(row => {
      var date = new Date(row[0]); // Assuming date in first column
      var today = new Date();
      return (today - date) / (1000 * 60 * 60 * 24) <= days;
    });
    var newSheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet('Timeline_' + days + 'd');
    newSheet.getRange(1, 1, filteredData.length, filteredData[0].length).setValues(filteredData);
  }
}

function sortClientDashboard() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Client Performance');
  var range = sheet.getDataRange();
  var ui = SpreadsheetApp.getUi();
  var result = ui.prompt('Sort by column (e.g., Ad Spend, CPC, CTR, CPL, CPQ) and order (ASC/DESC):', ui.ButtonSet.OK_CANCEL);
  if (result.getSelectedButton() == ui.Button.OK) {
    var input = result.getResponseText().split(',');
    var column = input[0].trim();
    var order = input[1].trim().toUpperCase();
    var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    var colIndex = headers.indexOf(column) + 1;
    if (colIndex > 0) {
      range.sort({column: colIndex, ascending: order === 'ASC'});
    } else {
      ui.alert('Invalid column name!');
    }
  }
}
