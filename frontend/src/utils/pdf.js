import { jsPDF } from 'jspdf'

export function exportTextPdf(title, content) {
  const doc = new jsPDF()
  doc.setFontSize(16)
  doc.text(title, 10, 10)
  doc.setFontSize(11)
  const lines = doc.splitTextToSize(content || '', 180)
  doc.text(lines, 10, 20)
  doc.save(`${title.toLowerCase().replace(/\s+/g, '-')}.pdf`)
}
