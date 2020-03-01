pragma solidity >=0.5.0 <0.5.12;
contract Order {
    uint8 food;
    string delivery_address;
    uint16 delivery_distance;
    string client;
    string tx_hash;
    uint128 order_time;
    uint128 delivery_time;
    uint128 expected_time;
    uint8 status;
    address restaurant;
    constructor (string memory new_client, string memory new_tx_hash, uint128 new_time, string memory new_delivery, uint16 new_dist, uint8 new_food, address new_restaurant) public {
        client = new_client;
        delivery_address = new_delivery;
        delivery_distance = new_dist;
        tx_hash = new_tx_hash;
        order_time = new_time;
        expected_time = order_time + 600;
        food = new_food;
        status = 1;
        restaurant = new_restaurant;
    }
    function add_delivery(string memory new_delivery, uint16 new_dist) public {
        require(msg.sender == restaurant);
        delivery_address = new_delivery;
        delivery_distance = new_dist;
    }
    function add_food(uint8 new_food) public {
        require(msg.sender == restaurant);
        food = new_food;
    }
    function get_food() public view returns (uint8) {
        return food;
    }
    function get_distance() public view returns (uint16) {
        return delivery_distance;
    }
    function get_distance_coords() public view returns (string memory) {
        return delivery_address;
    }
    function get_tx_hash() public view returns (string memory) {
        return tx_hash;
    }
    function get_client() public view returns (string memory) {
        return client;
    }
    function get_info() public view returns (uint8, uint16, uint128, uint128, uint128, string memory, string memory, string memory, uint8) {
        return (food, delivery_distance, order_time, delivery_time, expected_time, delivery_address, tx_hash, client, status);
    }
    function set_started_delivery() public {
        require(msg.sender == restaurant);
        status = 2;
    }
    function set_completed(uint128 time) public {
        require(msg.sender == restaurant);
        status = 3;
        delivery_time = time;
    }
}

contract Stats {
    uint[100] FoodStats;
    uint16 ZoneStats;
    uint cnt_orders;
    address[] orders;
    mapping(address=>uint8) completed_orders;
    uint completed_orders_cnt;
    address owner;
    constructor () public {
        cnt_orders = 0;
        for (uint i = 0; i < 100; i++) {
            FoodStats[i] = 0;
        }
        completed_orders_cnt = 0;
        owner = msg.sender;
    }
    function add_order(address order) public {
        require(completed_orders[order] == 0 && msg.sender == owner);
        Order tmp = Order(order);
        cnt_orders += 1;
        FoodStats[tmp.get_food()] += 1;
        ZoneStats = uint16((uint256(ZoneStats) * (cnt_orders - 1) + uint256(tmp.get_distance())) / cnt_orders);
        orders.push(order);
        completed_orders[order] = 1;
        
    }
    function get_stats() public view returns (uint16, uint[100] memory, uint, uint, address[] memory) {
        return (ZoneStats, FoodStats, cnt_orders, completed_orders_cnt, orders);
    }
    function get_orders() public view returns (address[] memory) {
        return orders;
    }
    function start_delivery(address order) public {
        require(completed_orders[order] == 1 && msg.sender == owner);
        completed_orders[order] = 2;
        Order tmp = Order(order);
        tmp.set_started_delivery();
    }
    function complete_order(address order, uint128 time) public {
        require(completed_orders[order] == 2 && msg.sender == owner);
        completed_orders[order] = 3;
        completed_orders_cnt += 1;
        Order tmp = Order(order);
        tmp.set_completed(time);
        
    }
    function get_order_info(address order) public view returns (uint, uint, uint, uint, uint, string memory, string memory, string memory, uint) {
        require(completed_orders[order] != 0);
        Order tmp = Order(order);
        return tmp.get_info();
    }
    
}