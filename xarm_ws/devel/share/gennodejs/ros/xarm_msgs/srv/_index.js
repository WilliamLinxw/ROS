
"use strict";

let SetControllerAnalogIO = require('./SetControllerAnalogIO.js')
let ConfigToolModbus = require('./ConfigToolModbus.js')
let Move = require('./Move.js')
let GetErr = require('./GetErr.js')
let TCPOffset = require('./TCPOffset.js')
let GetAnalogIO = require('./GetAnalogIO.js')
let SetLoad = require('./SetLoad.js')
let ClearErr = require('./ClearErr.js')
let MoveAxisAngle = require('./MoveAxisAngle.js')
let SetToolModbus = require('./SetToolModbus.js')
let SetInt16 = require('./SetInt16.js')
let SetDigitalIO = require('./SetDigitalIO.js')
let GetDigitalIO = require('./GetDigitalIO.js')
let SetAxis = require('./SetAxis.js')
let GetControllerDigitalIO = require('./GetControllerDigitalIO.js')
let GripperState = require('./GripperState.js')
let GripperConfig = require('./GripperConfig.js')
let GripperMove = require('./GripperMove.js')

module.exports = {
  SetControllerAnalogIO: SetControllerAnalogIO,
  ConfigToolModbus: ConfigToolModbus,
  Move: Move,
  GetErr: GetErr,
  TCPOffset: TCPOffset,
  GetAnalogIO: GetAnalogIO,
  SetLoad: SetLoad,
  ClearErr: ClearErr,
  MoveAxisAngle: MoveAxisAngle,
  SetToolModbus: SetToolModbus,
  SetInt16: SetInt16,
  SetDigitalIO: SetDigitalIO,
  GetDigitalIO: GetDigitalIO,
  SetAxis: SetAxis,
  GetControllerDigitalIO: GetControllerDigitalIO,
  GripperState: GripperState,
  GripperConfig: GripperConfig,
  GripperMove: GripperMove,
};
