local device = DeviceModule.create();
function toast(msg)
  device:broadcast('com.milayun.action.receiver', {ac='TOAST', msg=msg});
end
function broadcast(action, param)
  device:broadcast(action, param);
end
function press(key)
  device:pressKey(key);
end
function click(table)
  device:click(table);
end
function exist(table)
  return device:exist(table);
end
function cmd(command)
  return device:cmd(command);
end
function sleep(millisecond)
  return device:sleep(millisecond);
end

function write_file(name, content)
  return device:writeFile(name, content);
end
function set_text(text, table)
  return device:setText(text, table);
end
function verify_code(table)
  return device:verifyCode(table);
end
function verify_error(id)
  return device:verifyError(id)
end

function repo(param)
  return device:repo(param);
end
local dkjson = require("dkjson");
--local args = dkjson.decode (device:args())
args = device:args();
local workDir = device:getWorkDir();

