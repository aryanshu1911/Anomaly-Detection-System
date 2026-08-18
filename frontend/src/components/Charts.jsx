import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, PieChart, Pie } from 'recharts';

const COLORS = {
  Critical: 'var(--color-critical)',
  High: 'var(--color-high)',
  Medium: 'var(--color-medium)',
  Low: 'var(--color-low)'
};

const PREDICTION_COLORS = {
  Normal: 'var(--color-normal)',
  Attack: 'var(--color-critical)'
};

export function SeverityBar({ alerts }) {
  const counts = { Critical: 0, High: 0, Medium: 0, Low: 0 };
  alerts.forEach(a => {
    if (counts[a.severity] !== undefined) counts[a.severity]++;
  });
  
  const data = Object.keys(counts).map(key => ({
    name: key,
    count: counts[key]
  }));

  return (
    <ResponsiveContainer width="100%" height={200}>
      <BarChart data={data}>
        <XAxis dataKey="name" stroke="var(--text-muted)" fontSize={11} tickLine={false} axisLine={false} />
        <Tooltip 
          cursor={{fill: 'var(--bg-surface-hover)'}}
          contentStyle={{ backgroundColor: 'var(--bg-surface)', borderColor: 'var(--border-color)', fontSize: '12px' }}
          itemStyle={{ color: 'var(--text-primary)' }}
        />
        <Bar dataKey="count" radius={[2, 2, 0, 0]}>
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[entry.name]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}

export function PredictionPie({ alerts }) {
  const counts = { Normal: 0, Attack: 0 };
  alerts.forEach(a => {
    if (a.prediction === 0) counts.Normal++;
    else counts.Attack++;
  });
  
  const data = [
    { name: 'Normal Traffic', value: counts.Normal },
    { name: 'Attack Traffic', value: counts.Attack }
  ].filter(d => d.value > 0);

  return (
    <ResponsiveContainer width="100%" height={200}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={80}
          paddingAngle={5}
          dataKey="value"
          stroke="none"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={PREDICTION_COLORS[entry.name === 'Normal Traffic' ? 'Normal' : 'Attack']} />
          ))}
        </Pie>
        <Tooltip 
          contentStyle={{ backgroundColor: 'var(--bg-surface)', borderColor: 'var(--border-color)', fontSize: '12px' }}
          itemStyle={{ color: 'var(--text-primary)' }}
        />
      </PieChart>
    </ResponsiveContainer>
  );
}
