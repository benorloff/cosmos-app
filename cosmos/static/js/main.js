$(document).ready(function () {
    M.AutoInit();
    const DateField = MaterialDateTimePicker.create($('#id_start_time'))
});

$(document).ready(function () {
    M.AutoInit();
    const DateField = MaterialDateTimePicker.create($('#id_end_time'))
});


const filterEl = document.querySelector('.dropdown-trigger');
const tooltipEls = document.querySelectorAll('.tooltipped');
M.Dropdown.init(filterEl, {
    alignment: 'bottom',
    coverTrigger: false,
    constrainWidth: false
});
M.Tooltip.init(tooltipEls);
