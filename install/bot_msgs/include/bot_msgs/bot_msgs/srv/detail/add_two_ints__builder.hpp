// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from bot_msgs:srv/AddTwoInts.idl
// generated code does not contain a copyright notice

#ifndef BOT_MSGS__SRV__DETAIL__ADD_TWO_INTS__BUILDER_HPP_
#define BOT_MSGS__SRV__DETAIL__ADD_TWO_INTS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "bot_msgs/srv/detail/add_two_ints__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace bot_msgs
{

namespace srv
{

namespace builder
{

class Init_AddTwoInts_Request_b
{
public:
  explicit Init_AddTwoInts_Request_b(::bot_msgs::srv::AddTwoInts_Request & msg)
  : msg_(msg)
  {}
  ::bot_msgs::srv::AddTwoInts_Request b(::bot_msgs::srv::AddTwoInts_Request::_b_type arg)
  {
    msg_.b = std::move(arg);
    return std::move(msg_);
  }

private:
  ::bot_msgs::srv::AddTwoInts_Request msg_;
};

class Init_AddTwoInts_Request_a
{
public:
  Init_AddTwoInts_Request_a()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AddTwoInts_Request_b a(::bot_msgs::srv::AddTwoInts_Request::_a_type arg)
  {
    msg_.a = std::move(arg);
    return Init_AddTwoInts_Request_b(msg_);
  }

private:
  ::bot_msgs::srv::AddTwoInts_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::bot_msgs::srv::AddTwoInts_Request>()
{
  return bot_msgs::srv::builder::Init_AddTwoInts_Request_a();
}

}  // namespace bot_msgs


namespace bot_msgs
{

namespace srv
{

namespace builder
{

class Init_AddTwoInts_Response_sum
{
public:
  Init_AddTwoInts_Response_sum()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::bot_msgs::srv::AddTwoInts_Response sum(::bot_msgs::srv::AddTwoInts_Response::_sum_type arg)
  {
    msg_.sum = std::move(arg);
    return std::move(msg_);
  }

private:
  ::bot_msgs::srv::AddTwoInts_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::bot_msgs::srv::AddTwoInts_Response>()
{
  return bot_msgs::srv::builder::Init_AddTwoInts_Response_sum();
}

}  // namespace bot_msgs

#endif  // BOT_MSGS__SRV__DETAIL__ADD_TWO_INTS__BUILDER_HPP_
