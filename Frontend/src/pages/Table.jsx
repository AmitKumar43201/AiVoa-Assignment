import { useNavigate } from 'react-router-dom'
import { useSelector, useDispatch  } from 'react-redux'
import { setForm} from '../redux/slices/formContext.js'

export default function QueryResultsTable() {
    const results = useSelector((state) => state.queryResults.results)
    const dispatch = useDispatch()
    const navigate = useNavigate()

    const handleOpenForm = (row) => {
        console.log("data of row", row)
        dispatch(setForm(row))
        navigate('/')
    }

    if (!results.length) return <div>No data avialable please ask agent to get desired data</div>

    return (
        <div style={{ fontFamily: 'Inter, sans-serif', background: '#fff', color: '#000', padding: '24px' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                    <tr style={{ borderBottom: '2px solid #000' }}>
                        <th style={th}>HCP Name</th>
                        <th style={th}>Interaction Type</th>
                        <th style={th}>Date</th>
                        <th style={th}>Time</th>
                        <th style={th}>Sentiment</th>
                        <th style={th}>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {results.map((row, index) => (
                        <tr key={index} style={{ borderBottom: '1px solid #000' }}>
                            <td style={td}>{row.hcp_name}</td>
                            <td style={td}>{row.interaction_type}</td>
                            <td style={td}>{row.date}</td>
                            <td style={td}>{row.time}</td>
                            <td style={td}>{row.sentiment}</td>
                            <td style={td}>
                                <button onClick={() => handleOpenForm(row)} style={btn}>Open Form</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}

const th = { textAlign: 'left', padding: '10px', fontWeight: 'bold' }
const td = { padding: '10px' }
const btn = { marginRight: '8px', padding: '4px 10px', cursor: 'pointer', fontFamily: 'Inter, sans-serif' }