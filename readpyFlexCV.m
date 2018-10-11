%read output of pyFlexCV, save in struct

fps = 29;        %set fps from movie properties

% X-data
filename = 'x.dat';         %import
M = csvread(filename);
M(M == 0) = NaN;            %replace 0 with NaN
data.x = M;


% Y-data
filename = 'y.dat';         %import
M = csvread(filename);
M(M == 0) = NaN;            %replace 0 with NaN
data.y = M;



f = max(data.y);
f = max(f);

data.y = abs(data.y - f);


%%% Plot and animate
pointsize = 10;
h=plot(data.x(1,:),data.y(1,:),'-gs','LineWidth',2,'MarkerSize',2);    %Profiles in cols, timesteps in rows, d.h. hier wird das zeitlich erste profil in handle "gespeichert"
xlim([300 700])
ylim([0 150])

for i=1: length(data.x) 
    set(h,'XData',data.x(i,:),'YData',data.y(i,:));        %animate here
    pause(1/fps); 
end




