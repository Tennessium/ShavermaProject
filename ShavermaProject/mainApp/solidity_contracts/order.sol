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
    function get_status() public view returns(uint8) {
        return status;
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