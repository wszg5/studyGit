str = repo({type='Number', status='normal', cate_id=args.repo_cate_id, interval='1', limit=args.number_count})
local numbers = dkjson.decode (str).result

if (args.clear=='是') then
  cmd("pm clear com.android.providers.contacts")
end

local content = "";
for i=1, #(numbers) do
    local number = numbers[i].number
    local name = numbers[i].name
    if(name == nil) then
    	name = number;
    end
    content = content .. name .. '----' .. number .. '\n'
end
write_file(workDir .. '/contact.txt', content);
broadcast('com.milayun.action.receiver', {ac='IMPORT_CONTACT', contact_file= workDir .. '/contact.txt'});