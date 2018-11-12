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
sensors = ["0x0283fdaf", "0x0281fe5f", "0x0268fc8f"];
axes = ["x", "y", "z"];

% t = h5read(filename, ['/' sensor_type '/' char(sensors(1)) '/t']);

figure();
for d=1:length(sensors)
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
    
    subplot(length(sensors),1,d);
    hold on;
    plot([1:length(diff_x)]/100, diff_x, 'r');
    plot([1:length(diff_y)]/100, diff_y, 'g');
    plot([1:length(diff_z)]/100, diff_z, 'b');
    hold off;
end

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
