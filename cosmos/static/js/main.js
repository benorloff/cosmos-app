const filterEl = document.querySelector('.dropdown-trigger');
const tooltipEls = document.querySelectorAll('.tooltipped');
M.Dropdown.init(filterEl, {
    alignment: 'bottom',
    coverTrigger: false,
    constrainWidth: false
});
M.Tooltip.init(tooltipEls);
