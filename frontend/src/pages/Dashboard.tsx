import { useMemo } from 'react'

const cards = [
  { title: 'Factures envoyées', value: '124' },
  { title: 'Acceptées', value: '117' },
  { title: 'Rejetées', value: '7' },
  { title: 'TVA du mois', value: '14 820 TND' }
]

export const Dashboard = () => {
  const statusColor = useMemo(() => ({ accepted: '#0a7d2c', rejected: '#b42318' }), [])

  return (
    <main style={{ fontFamily: 'Arial, sans-serif', maxWidth: 900, margin: '2rem auto' }}>
      <h1>Plateforme SaaS e-Facturation Tunisie</h1>
      <p>Intermédiaire conforme pour la génération, signature, transmission et archivage légal.</p>
      <section style={{ display: 'grid', gridTemplateColumns: 'repeat(2,1fr)', gap: 12 }}>
        {cards.map((card) => (
          <div key={card.title} style={{ border: '1px solid #ddd', borderRadius: 8, padding: 12 }}>
            <strong>{card.title}</strong>
            <p>{card.value}</p>
          </div>
        ))}
      </section>
      <section style={{ marginTop: 20 }}>
        <h2>Statuts API gouvernementale</h2>
        <ul>
          <li style={{ color: statusColor.accepted }}>FAC-2026-009 — ACCEPTED</li>
          <li style={{ color: statusColor.rejected }}>FAC-2026-010 — REJECTED (format XML invalide)</li>
        </ul>
      </section>
    </main>
  )
}
