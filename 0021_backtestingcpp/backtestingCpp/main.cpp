#include <iostream>
#include <cstring>
#include <hdf5.h>
#include "Sma.h"


int main(int, char**) {
	
    std::string symbol = "BTCUSDT";
	std::string exchange = "D:\\source_code\\backtestingCpp\\data\\binance.h5";
	std::string timeframe = "5m";

	char* symbol_char = (char*)malloc(symbol.length() + 1);
	char* exchange_char = (char*)malloc(exchange.length() + 1);
	char* tf_char = (char*)malloc(timeframe.length() + 1);

	strcpy_s(symbol_char, symbol.length() + 1, symbol.c_str());
	strcpy_s(exchange_char, exchange.length() + 1, exchange.c_str());
	strcpy_s(tf_char, timeframe.length() + 1, timeframe.c_str());

	std::cout << "Symbol: " << symbol_char << std::endl;
	std::cout << "Exchange: " << exchange_char << std::endl;
	std::cout << "Timeframe: " << tf_char << std::endl;


    Sma sma(exchange_char, symbol_char, tf_char, 0, 1630074127000);
    sma.execute_backtest(15, 8);
    printf("%f | %f\n", sma.pnl, sma.max_dd);
	free(symbol_char);
	free(exchange_char);
	free(tf_char);
}