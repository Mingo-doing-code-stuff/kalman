clf('reset');
disp('-------------------------------------------------------------');
disp('Kalman Filter Beispiel (diskreter Kalman Filter)');
disp('Messwerte eines Gyroskopes auf der X-Achse in 131LSB/°/s');

% 10 Messwerte der X-Achse des Gyroskopes in Ruhe
gyroX = [-217;-195;-192;-199;-200;-192;-206;-195;-208;-208];

% Anzahl der Messwerte
gyroXarrSize = size(gyroX,1);

% Median der Messwerte
gyroXmedian = median(gyroX);

% Temperaturbias (Drift) berechnen:
% >> Median ueber alle Werte bei Ruhelage
% >> Subtraktion auf die Messwerte anwenden
gyroXbias = 0; %Feld zuruecksetzen
for j = 1:gyroXarrSize
    % Median zur Korrektur des Temperaturdriftes subtrahieren:
    gyroXbias(j) = gyroX(j)-gyroXmedian;
end

% Varianz der Messergebnisse
% (0.1 einsetzen fuer ein anschauliches Beispiel
% zur Anpassung des Kalman Gain und der Fehlerkovarianz)
% (var(gyroXbias) fuer ein anschauliches Beispiel
% zur Exaktheit des Kalman Filters)
gyroXbiasVarianz = 0.1;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Anwendung der Filteriterationen%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Varianz der Messergebnisse wird durch R dargestellt
R = gyroXbiasVarianz;

% Einheitsmatrix, hier numerisch, deshalb = 1
I=1;

% Initiale Vorbelegung
filterVals = 0; % Zuruecksetzen des Filterarrays
kalmanVals = 0; % Zuruecksetzen des Kalman Gain Arrays
xkSub1 = 0;
xk = xkSub1; % Vorheriger Messwert unbekannt, deshalb 0

% Fehlerkovarianz am Anfang 1 und nicht 0,
% da normalerweise immer ein Messrauschen vorhanden ist
PkSub1 = 1;
Pk = PkSub1;

% Iteration 1: Erste Schaetzung
zk = gyroXbias(1);
Kk = Pk/(Pk+R);
kalmanVals(1) = Kk;
xk = xk + Kk*(zk-xk);
filterVals(1) = xk;
Pk = (I-Kk)*Pk;

%Iteration 2 bis gyroXarrSize
for j = 2:1:gyroXarrSize
    
    %Vorhersage
    zk = gyroXbias(j); %Aktuelle Messung
    xk = filterVals(j-1); %xk = xk-1;
    
    % Korrektur
    Kk = Pk/(Pk+R);
    kalmanVals(j) = Kk;
    xk = xk + Kk*(zk-xk);
    filterVals(j) = xk;
    Pk = (I-Kk)*Pk;
end

% -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

% Graph plotten
hold on;
bar(kalmanVals, 'DisplayName', 'Kk: Kalman Gain','LineStyle', '-','FaceColor', [0 .75 1], 'EdgeColor','b');
plot(gyroXbias,'-','DisplayName','zk: Messwerte','Color','red');
plot(filterVals,'Color','green','LineWidth',2,'DisplayName', 'xk: gefilterte Werte')
line([0,gyroXarrSize],[0,0],'Color','blue','DisplayName','reales Signal')

% Legende anzeigen
legend('show');

% Achsenbeschriftung
xlabel('Zeit in ms');
ylabel('Winkelgeschwindigkeit in °/s','LineWidth',2);

% Plot Raender entfernen
set(gca,'LooseInset',get(gca,'TightInset'))

% Skalierung Y-Achse anpassen
yticks = get(gca,'YTick');
set(gca,'yticklabel',round(yticks/131.*100)/100);

% Bereich X-Achse anpassen
xlim([0 gyroXarrSize]);