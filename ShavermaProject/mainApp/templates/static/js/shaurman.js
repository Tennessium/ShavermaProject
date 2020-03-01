orders_container = document.getElementById('orders');
copters_container = document.getElementById('copters');

var orders = [];
var copters = [];


function send_drone(sID, zID, address) {
    removeElement('copter' + sID.toString());
    console.log(address);
    setTimeout(function () {
        let req = new XMLHttpRequest();
        req.open('post', '/shaurman?l=send&sID=' + sID.toString() + '&zID=' + zID.toString() + '&address=' + address, true);
        req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        req.send('l=send&sID=' + sID.toString() + '&zID=' + zID.toString() + '&address=' + address);

    }, 1);
}

const order_template = '<div draggable="true" id="ID" class="zakaz"><div class="both"><div class="geo">GEO</div><div class="order">ORDER</div><div style=" text-overflow: ellipsis; overflow: hidden;" class="order">ADDRESS</div></div></div>';
const copter_template = '<div id="ID" class="copter"><div><div class="both"><div class="geo">GEO</div><div class="order"></div></div></div><div id="zID"></div></div>';
const za_template = '<div class="both"><div class="geo">GEO</div><div class="order">ORDER</div><div class="send" onclick="send_drone(sID, zID, \'ADDRESS\')">Отправить</div>';

var order_taken = null;

function render_orders() {
    orders_container.innerHTML = '';
    orders.forEach(function (e) {
        orders_container.innerHTML += order_template
            .replace('GEO', e['geo']).replace('ORDER', e['order'])
            .replace('ID', 'order' + e['#'].toString())
            .replace('ADDRESS', e['address']);
    });
    setTimeout(function () {
        orders.forEach(function (el) {
            let curr_element = document.getElementById('order' + el['#']);
            curr_element.ondragstart = function (e) {
                order_taken = el;
            };
            curr_element.ondragend = function (e) {
                console.log(order_taken);
                order_taken = null
            };
        });
    }, 1);
}

function render_copters() {
    copters_container.innerHTML = '';
    copters.forEach(function (e) {
        copters_container.innerHTML += copter_template.replace('GEO', e['id']).replace('zID', 'copter' + e['#'] + 'z')
            .replace('ID', 'copter' + e['#']);
    });
    setTimeout(function () {
        copters.forEach(function (el) {
            let curr_element = document.getElementById('copter' + el['#']);
            curr_element.ondragleave = function (e) {
                if (e.screenX === 0 && e.screenY === 0 && e.clientX === 0 && e.clientY === 0) {
                    removeElement('order' + order_taken['#']);
                    document.getElementById('copter' + el['#'] + 'z').innerHTML = za_template
                        .replace('GEO', order_taken['geo'])
                        .replace('ORDER', order_taken['order'])
                        .replace('sID', el['#'])
                        .replace('ADDRESS', order_taken['address'])
                        .replace('zID', order_taken['#']);
                }
            };
        });
    }, 1);
}

function removeElement(elementId) {
    var element = document.getElementById(elementId);
    element.parentNode.removeChild(element);
}

function render_all() {
    render_copters();
    render_orders();
}

var busy = false;

function update() {
    if (!busy) {
        busy = true;
        console.log('busy is true');
        let req = new XMLHttpRequest();
        req.open('post', '/shaurman?l=check', true);
        req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        req.onreadystatechange = function () {
            if (req.responseText === 'True') {
                req.open('post', '/shaurman?l=drones', true);
                req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                req.onreadystatechange = function () {
                    copters = JSON.parse(req.responseText);
                    req.open('post', '/shaurman?l=orders', true);
                    req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                    req.onreadystatechange = function () {
                        orders = JSON.parse(req.responseText);
                        render_all();
                        busy = false;
                        console.log('busy is false');
                    };
                    req.send('l=orders');
                };
                req.send('l=drones');
            } else {
                busy = false;
            }
        };
        req.send('l=check');
    }
    console.log('busy');
}


setInterval(update, 3000);

