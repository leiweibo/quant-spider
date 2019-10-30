CREATE DATABASE IF NOT EXISTS db_quant precision 'us';

USE db_quant;



create table t_fund(
    fund_timestamp timestamp,
    fund_symbol binary(20),
    fund_name binary(128)
);

create table t_fund_net_value(
    net_value_timestamp timestamp,
    fund_symbol binary(20),
    fund_date timestamp,
    fund_net_value float,
    fund_accu_net_value float,
    redemption_status binary(36),
    subscription_status binary(36)
);

create table t_cache(
    cache_timestamp timestamp,
    c_key binary(20),
    c_type binary(20)
);


create table t_stock(
    stock_timestamp timestamp,
    stock_symbol binary(20),
    stock_date int,
    stock_open int,
    stock_close int,
    stock_low int,
    stock_high int,
    stock_amount BIGINT,
    stock_vol BIGINT);