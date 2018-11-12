close all
clear all
clc

filename = uigetfile('.h5');

info = h5info(filename);
uuid = h5readatt(filename, '/', '_uuid');
disp( [filename ' → uuid ' uuid{:}]);
try
    info_start_event = h5info(filename, '/EVENT/START_SESSION');
    start_attribute_names  =  {info_start_event.Attributes.Name};
    for attribute_name = start_attribute_names
        attribute_value = h5readatt(filename, '/EVENT/START_SESSION', attribute_name{1});
        disp([attribute_name{1} ' → ' attribute_value{1}])
    end
end

sensor_type = 'ACCELEROMETER_3D';
sens_r = ["0x0283fdaf", "0x0281fe5f", "0x0268fc8f"];
sens_l = ["0x02a3fdaf", "0x02a1fe5f", "0x0268fe8f"];
axes = ["x", "y", "z"];

t = h5read(filename, ['/' sensor_type '/' char(sens_r(1)) '/t']);

% plot the sum of 3 sensors (right arm)
figure();
for ax=1:length(axes)
    data = [0 zeros(size(t))];
    min_l = length(data);
    for d=1:length(sens_r)
        x = h5read(filename, ['/' sensor_type '/' char(sens_r(d)) '/' char(axes(ax)) '/v']);
        min_l = min(min_l, length(x));
        x = x(1:min_l);
        
        d1 = [0 x];
        d2 = [x 0];
        diff_square = (d1-d2).^2;
        
        data = data + diff_square;
    end
    
    subplot(length(axes),1,ax);
    plot([1:length(data)]/100, data);
    title(axes(ax));
end



% plot the sum of 6 sensors (both arms)
s = [sens_r sens_l];
figure();
for ax=1:length(axes)
    data = [0 zeros(size(t))];
    min_l = length(data);
    for d=1:length(s)
        x = h5read(filename, ['/' sensor_type '/' char(s(d)) '/' char(axes(ax)) '/v']);
        min_l = min(min_l, length(x));
        x = x(1:min_l);
        
        d1 = [0 x];
        d2 = [x 0];
        diff_square = (d1-d2).^2;
        
        data = data + diff_square;
    end
    
    subplot(length(axes),1,ax);
    plot([1:length(data)]/100, data);
    title(axes(ax));
end








%%
sensors2 = ["0x02a3fdaf", "0x02a1fe5f", "0x0268fe8f"];
figure();
for d=1:length(sensors2)
    x = h5read(filename, ['/' sensor_type '/' char(sensors(d)) '/x/v']);
    y = h5read(filename, ['/' sensor_type '/' char(sensors(d)) '/y/v']);
    z = h5read(filename, ['/' sensor_type '/' char(sensors(d)) '/z/v']);
    
    x1 = [0 x];
    x2 = [x 0];
    diff_x = x1-x2;
    
    y1 = [0 y];
    y2 = [y 0];
    diff_y = y1-y2;
    
    z1 = [0 z];
    z2 = [z 0];
    diff_z = z1-z2;
    
    subplot(length(sensors2),1,d);
    hold on;
    plot([1:length(diff_x)]/100, diff_x, 'r');
    plot([1:length(diff_y)]/100, diff_y, 'g');
    plot([1:length(diff_z)]/100, diff_z, 'b');
    hold off;
end
