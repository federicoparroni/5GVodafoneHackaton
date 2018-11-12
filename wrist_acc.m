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
sensor_position = '0x0283fdaf';
ecg_t = h5read(filename, ['/' sensor_type '/' sensor_position '/t']);
x = h5read(filename, ['/' sensor_type '/' sensor_position '/x/v']);
y = h5read(filename, ['/' sensor_type '/' sensor_position '/y/v']);
z = h5read(filename, ['/' sensor_type '/' sensor_position '/z/v']);

%ecg_t = ecg_t(5:end);
ecg_t = [0 ecg_t];
x1 = [0 x];
x2 = [x 0];
diff_x = x1-x2;

y1 = [0 y];
y2 = [y 0];
diff_y = y1-y2;

z1 = [0 z];
z2 = [z 0];
diff_z = z1-z2;

avg_x = zeros(1,length(x)-5);
for i=5:length(x)
    avg_x(i-4) = (x(i)+x(i-1)+x(i-2)+x(i-3)+x(i-4))/5;
end

avg_y = zeros(1,length(y)-5);
for i=5:length(y)
    avg_y(i-4) = (y(i)+y(i-1)+y(i-2)+y(i-3)+y(i-4))/5;
end

avg_z = zeros(1,length(z)-5);
for i=5:length(z)
    avg_z(i-4) = (z(i)+z(i-1)+z(i-2)+z(i-3)+z(i-4))/3;
end


%% plot
figure();
ax1 = subplot(4,1,1);
plot([1:length(diff_x)]/100, diff_x.^2);
ax2 = subplot(4,1,2);
plot([1:length(diff_y)]/100, diff_y.^2);
ax3 = subplot(4,1,3);
plot([1:length(diff_z)]/100, diff_z.^2);

ax4 = subplot(4,1,4);
plot([1:length(diff_x)]/100, diff_x.^2+diff_y.^2+diff_z.^2);
linkaxes([ax1, ax2, ax3, ax4], 'x')

%% 
% ax1 = subplot(3,1,1);
% plot(ecg_t/100, avg_x)
% ax2 = subplot(3,1,2);
% plot(ecg_t/100, avg_y)
% ax3 = subplot(3,1,3);
% plot(ecg_t/100, avg_z)
% linkaxes([ax1, ax2, ax3], 'x')