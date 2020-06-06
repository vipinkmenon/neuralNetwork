`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 07.04.2019 20:57:54
// Design Name: 
// Module Name: top_layer
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////
`include "include.v"

module zyNet #(
    parameter integer C_S_AXI_DATA_WIDTH    = 32,
    parameter integer C_S_AXI_ADDR_WIDTH    = 5
)
(
    //Clock and Reset
    input                                   s_axi_aclk,
    input                                   s_axi_aresetn,
    //AXI Stream interface
    input [`dataWidth-1:0]                  axis_in_data,
    input                                   axis_in_data_valid,
    output                                  axis_in_data_ready,
);


assign axis_in_data_ready = 1'b1;

wire reset;

assign reset = ~s_axi_aresetn;

localparam IDLE = 'd0,
           SEND = 'd1;
wire [`numNeuronLayer1-1:0] o1_valid;
wire [`numNeuronLayer1*`dataWidth-1:0] x1_out;
reg [`numNeuronLayer1*`dataWidth-1:0] holdData_1;
reg [`dataWidth-1:0] out_data_1;
reg data_out_valid_1;

Layer_1 #(.NN(`numNeuronLayer1),.numWeight(`numWeightLayer1),.dataWidth(`dataWidth),.layerNum(1),.sigmoidSize(`sigmoidSize),.weightIntWidth(`weightIntWidth),.actType(`Layer1ActType)) l1(
	.clk(s_axi_aclk),
	.rst(reset),
	.weightValid(weightValid),
	.biasValid(biasValid),
	.weightValue(weightValue),
	.biasValue(biasValue),
	.config_layer_num(config_layer_num),
	.config_neuron_num(config_neuron_num),
	.x_valid(axis_in_data_valid),
	.x_in(axis_in_data),
	.o_valid(o1_valid),
	.x_out(x1_out)
);

//State machine for data pipelining

reg       state_1;
integer   count_1;
always @(posedge s_axi_aclk)
begin
    if(reset)
    begin
        state_1 <= IDLE;
        count_1 <= 0;
        data_out_valid_1 <=0;
    end
    else
    begin
        case(state_1)
            IDLE: begin
                count_1 <= 0;
                data_out_valid_1 <=0;
                if (o1_valid[0] == 1'b1)
                begin
                    holdData_1 <= x1_out;
                    state_1 <= SEND;
                end
            end
            SEND: begin
                out_data_1 <= holdData_1[`dataWidth-1:0];
                holdData_1 <= holdData_1>>`dataWidth;
                count_1 <= count_1 +1;
                data_out_valid_1 <= 1;
                if (count_1 == `numNeuronLayer1)
                begin
                    state_1 <= IDLE;
                    data_out_valid_1 <= 0;
                end
            end
        endcase
    end
end

wire [`numNeuronLayer2-1:0] o2_valid;
wire [`numNeuronLayer2*`dataWidth-1:0] x2_out;
reg [`numNeuronLayer2*`dataWidth-1:0] holdData_2;
reg [`dataWidth-1:0] out_data_2;
reg data_out_valid_2;

Layer_2 #(.NN(`numNeuronLayer2),.numWeight(`numWeightLayer2),.dataWidth(`dataWidth),.layerNum(2),.sigmoidSize(`sigmoidSize),.weightIntWidth(`weightIntWidth),.actType(`Layer2ActType)) l2(
	.clk(s_axi_aclk),
	.rst(reset),
	.weightValid(weightValid),
	.biasValid(biasValid),
	.weightValue(weightValue),
	.biasValue(biasValue),
	.config_layer_num(config_layer_num),
	.config_neuron_num(config_neuron_num),
	.x_valid(data_out_valid_1),
	.x_in(out_data_1),
	.o_valid(o2_valid),
	.x_out(x2_out)
);

//State machine for data pipelining

reg       state_2;
integer   count_2;
always @(posedge s_axi_aclk)
begin
    if(reset)
    begin
        state_2 <= IDLE;
        count_2 <= 0;
        data_out_valid_2 <=0;
    end
    else
    begin
        case(state_2)
            IDLE: begin
                count_2 <= 0;
                data_out_valid_2 <=0;
                if (o2_valid[0] == 1'b1)
                begin
                    holdData_2 <= x2_out;
                    state_2 <= SEND;
                end
            end
            SEND: begin
                out_data_2 <= holdData_2[`dataWidth-1:0];
                holdData_2 <= holdData_2>>`dataWidth;
                count_2 <= count_2 +1;
                data_out_valid_2 <= 1;
                if (count_2 == `numNeuronLayer2)
                begin
                    state_2 <= IDLE;
                    data_out_valid_2 <= 0;
                end
            end
        endcase
    end
end

wire [`numNeuronLayer3-1:0] o3_valid;
wire [`numNeuronLayer3*`dataWidth-1:0] x3_out;
reg [`numNeuronLayer3*`dataWidth-1:0] holdData_3;
reg [`dataWidth-1:0] out_data_3;
reg data_out_valid_3;

Layer_3 #(.NN(`numNeuronLayer3),.numWeight(`numWeightLayer3),.dataWidth(`dataWidth),.layerNum(3),.sigmoidSize(`sigmoidSize),.weightIntWidth(`weightIntWidth),.actType(`Layer3ActType)) l3(
	.clk(s_axi_aclk),
	.rst(reset),
	.weightValid(weightValid),
	.biasValid(biasValid),
	.weightValue(weightValue),
	.biasValue(biasValue),
	.config_layer_num(config_layer_num),
	.config_neuron_num(config_neuron_num),
	.x_valid(data_out_valid_2),
	.x_in(out_data_2),
	.o_valid(o3_valid),
	.x_out(x3_out)
);

//State machine for data pipelining

reg       state_3;
integer   count_3;
always @(posedge s_axi_aclk)
begin
    if(reset)
    begin
        state_3 <= IDLE;
        count_3 <= 0;
        data_out_valid_3 <=0;
    end
    else
    begin
        case(state_3)
            IDLE: begin
                count_3 <= 0;
                data_out_valid_3 <=0;
                if (o3_valid[0] == 1'b1)
                begin
                    holdData_3 <= x3_out;
                    state_3 <= SEND;
                end
            end
            SEND: begin
                out_data_3 <= holdData_3[`dataWidth-1:0];
                holdData_3 <= holdData_3>>`dataWidth;
                count_3 <= count_3 +1;
                data_out_valid_3 <= 1;
                if (count_3 == `numNeuronLayer3)
                begin
                    state_3 <= IDLE;
                    data_out_valid_3 <= 0;
                end
            end
        endcase
    end
end

wire [`numNeuronLayer4-1:0] o4_valid;
wire [`numNeuronLayer4*`dataWidth-1:0] x4_out;
reg [`numNeuronLayer4*`dataWidth-1:0] holdData_4;
reg [`dataWidth-1:0] out_data_4;
reg data_out_valid_4;

Layer_4 #(.NN(`numNeuronLayer4),.numWeight(`numWeightLayer4),.dataWidth(`dataWidth),.layerNum(4),.sigmoidSize(`sigmoidSize),.weightIntWidth(`weightIntWidth),.actType(`Layer4ActType)) l4(
	.clk(s_axi_aclk),
	.rst(reset),
	.weightValid(weightValid),
	.biasValid(biasValid),
	.weightValue(weightValue),
	.biasValue(biasValue),
	.config_layer_num(config_layer_num),
	.config_neuron_num(config_neuron_num),
	.x_valid(data_out_valid_3),
	.x_in(out_data_3),
	.o_valid(o4_valid),
	.x_out(x4_out)
);

//State machine for data pipelining

reg       state_4;
integer   count_4;
always @(posedge s_axi_aclk)
begin
    if(reset)
    begin
        state_4 <= IDLE;
        count_4 <= 0;
        data_out_valid_4 <=0;
    end
    else
    begin
        case(state_4)
            IDLE: begin
                count_4 <= 0;
                data_out_valid_4 <=0;
                if (o4_valid[0] == 1'b1)
                begin
                    holdData_4 <= x4_out;
                    state_4 <= SEND;
                end
            end
            SEND: begin
                out_data_4 <= holdData_4[`dataWidth-1:0];
                holdData_4 <= holdData_4>>`dataWidth;
                count_4 <= count_4 +1;
                data_out_valid_4 <= 1;
                if (count_4 == `numNeuronLayer4)
                begin
                    state_4 <= IDLE;
                    data_out_valid_4 <= 0;
                end
            end
        endcase
    end
end


endmodule