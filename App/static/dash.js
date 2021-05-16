const orderList = document.querySelector(".order-list");
const btnWrap = document.querySelector(".button-wrapper");

class OrderManager {
  constructor() {
    this.orders = [];
    this.currentOrders = new Map();
    this.resetActive();

    this.socket = io();

    this.socket.on("orders", this.updateOrders);
    this.socket.on("connect", () => console.info("Socket connected!"));
  }
  set activeOrder(order) {
    if (order.number == this.activeOrder) return;
    if (this.activeOrder !== null)
      this.currentOrders.get(this.activeOrder).classList.remove("active");
    this.currentOrders.get(order.number).classList.add("active");
    this.updateDOMItemList(order);
    this._active = order.number;
  }
  get activeOrder() {
    return this._active;
  }
  resetActive = () => {
    this._active = null;
  };
  updateDOMItemList = (order) => {
    const orderTable = document.createElement("table");
    orderTable.classList.add("order-table");
    orderTable.insertAdjacentHTML(
      "afterbegin",
      "<th>Item</th><th>Quantity</th><th></th>"
    );

    for (const [itemName, itemCount] of Object.entries(order.items)) {
      const tableRow = document.createElement("tr");
      const unStock = document.createElement("td");
      unStock.classList.add("notInStock", "ui", "icon");
      unStock.setAttribute("data-tooltip", `Mark ${itemName} as out of stock`);
      unStock.setAttribute("data-position", "right center");
      unStock.innerHTML = `<i class="times icon"></i>`;
      tableRow.insertAdjacentHTML(
        "afterbegin",
        `<td>${itemName}</td><td>${itemCount}</td>`
      );
      tableRow.appendChild(unStock);
      orderTable.appendChild(tableRow);
    }
    document.querySelector(".table-wrapper").replaceChildren(orderTable);

    const readyBtn = document.createElement("button");
    const pickUpBtn = document.createElement("button");
    readyBtn.classList.add("ui", "button");
    pickUpBtn.classList.add("ui", "button", "pickUpBtn", "hidden");
    readyBtn.innerText = "Ready for pickup!";
    pickUpBtn.innerText = `Pick up! PIN: ${order.pin}`;
    readyBtn.addEventListener("click", this.markedAsReady);
    pickUpBtn.addEventListener("click", this.markedAsPickeUp);
    btnWrap.replaceChildren(readyBtn, pickUpBtn);
  };
  markedAsReady = (e) => {
    this.socket.emit("ready", this.activeOrder);
    e.target.classList.add("hidden");
    document.querySelector(".pickUpBtn.hidden").classList.remove("hidden");
  };
  markedAsPickeUp = (e) => {
    this.socket.emit("pickedup", this.activeOrder);
    location.reload();
  };
  addOrder = (order) => {
    this.orders.push(order);
    const orderDiv = document.createElement("div");
    this.currentOrders.set(order.number, orderDiv);
    if (this.activeOrder === null) this.activeOrder = order;
    orderDiv.innerText = `Order #${order.number}`;
    orderDiv.addEventListener("click", (e) => {
      this.activeOrder = order;
    });
    orderList.insertAdjacentElement("beforeend", orderDiv);
  };

  updateOrders = (updatedOrders) => {
    for (const order of updatedOrders) {
      if (this.currentOrders.has(order.number)) continue;
      this.addOrder(order);
    }
  };
}

const orderManager = new OrderManager();
