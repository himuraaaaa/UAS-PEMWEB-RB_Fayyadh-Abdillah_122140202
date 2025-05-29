import React, { useEffect, useState } from 'react';
import { getAppointments, getBarbers, getServices, updateAppointment, deleteAppointment } from '../api';
import { Modal, Button, Tag, message } from 'antd';
import { useNavigate } from 'react-router-dom';
import { ArrowLeftOutlined } from '@ant-design/icons';
import './Booking/BookingPages.css';

const statusColors = {
  pending: 'gold',
  confirmed: 'blue',
  completed: 'green',
  cancelled: 'red'
};

const UserAppointments = () => {
  const [appointments, setAppointments] = useState([]);
  const [barbers, setBarbers] = useState([]);
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editModal, setEditModal] = useState({ open: false, apt: null });
  const [cancelId, setCancelId] = useState(null);
  const [form, setForm] = useState({ date: '', time: '', notes: '' });
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAll = async () => {
      setLoading(true);
      try {
        const [aptRes, barbersRes, servicesRes] = await Promise.all([
          getAppointments(),
          getBarbers(),
          getServices()
        ]);
        setAppointments(aptRes.data.data);
        setBarbers(barbersRes.data.data);
        setServices(servicesRes.data.data);
      } catch (err) {
        message.error('Failed to load appointments');
      }
      setLoading(false);
    };
    fetchAll();
  }, []);

  const getBarberName = (id) => barbers.find(b => b.id === id)?.name || 'N/A';
  const getServiceName = (id) => services.find(s => s.id === id)?.name || 'N/A';

  const handleEdit = (apt) => {
    setForm({
      date: apt.appointment_date.split('T')[0],
      time: apt.appointment_date.split('T')[1]?.slice(0,5) || '',
      notes: apt.notes || ''
    });
    setEditModal({ open: true, apt });
  };

  const handleEditSave = async () => {
    const { apt } = editModal;
    const appointment_date = new Date(`${form.date}T${form.time}`).toISOString();
    try {
      await updateAppointment(apt.id, { appointment_date, notes: form.notes });
      message.success('Appointment updated!');
      setEditModal({ open: false, apt: null });
      // Refresh
      const res = await getAppointments();
      setAppointments(res.data.data);
    } catch {
      message.error('Failed to update appointment');
    }
  };

  const handleCancel = (id) => setCancelId(id);
  const confirmCancel = async () => {
    try {
      await deleteAppointment(cancelId);
      message.success('Appointment cancelled');
      setCancelId(null);
      // Refresh
      const res = await getAppointments();
      setAppointments(res.data.data);
    } catch {
      message.error('Failed to cancel appointment');
    }
  };

  if (loading) return <div style={{textAlign:'center',marginTop:40}}>Loading...</div>;
  if (!appointments.length) return (
    <div style={{textAlign:'center',marginTop:40}}>
      <Button icon={<ArrowLeftOutlined />} onClick={()=>navigate('/')} style={{marginBottom:24}}>Back to Home</Button>
      You have no appointments yet.
    </div>
  );

  return (
    <div className="user-appointments" style={{maxWidth:900,margin:'40px auto',background:'#fff',borderRadius:12,padding:24,boxShadow:'0 2px 16px rgba(0,0,0,0.07)'}}>
      <div style={{display:'flex',alignItems:'center',marginBottom:24}}>
        <Button icon={<ArrowLeftOutlined />} onClick={()=>navigate('/')} style={{marginRight:16}}>
          Back
        </Button>
        <h2 style={{margin:0, fontWeight:700, fontSize:28, color:'var(--primary-color)'}}>My Appointments</h2>
      </div>
      <div style={{overflowX:'auto'}}>
      <table style={{width:'100%',borderCollapse:'collapse',minWidth:700}}>
        <thead>
          <tr style={{background:'var(--dark-color)',color:'#fff'}}>
            <th style={{padding:10}}>Date</th>
            <th style={{padding:10}}>Time</th>
            <th style={{padding:10}}>Barber</th>
            <th style={{padding:10}}>Service</th>
            <th style={{padding:10}}>Status</th>
            <th style={{padding:10}}>Notes</th>
            <th style={{padding:10}}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {appointments.map(apt => (
            <tr key={apt.id} style={{borderBottom:'1px solid #eee'}}>
              <td style={{padding:10}}>{new Date(apt.appointment_date).toLocaleDateString()}</td>
              <td style={{padding:10}}>{new Date(apt.appointment_date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</td>
              <td style={{padding:10}}>{getBarberName(apt.barber_id)}</td>
              <td style={{padding:10}}>{getServiceName(apt.service_id)}</td>
              <td style={{padding:10}}><Tag color={statusColors[apt.status]}>{apt.status?.toUpperCase()}</Tag></td>
              <td style={{padding:10}}>{apt.notes}</td>
              <td style={{padding:10}}>
                {(apt.status === 'pending' || apt.status === 'confirmed') && (
                  <>
                    <Button size="small" style={{marginRight:8}} onClick={()=>handleEdit(apt)}>Edit</Button>
                    <Button size="small" danger onClick={()=>handleCancel(apt.id)}>Cancel</Button>
                  </>
                )}
                {(apt.status === 'completed' || apt.status === 'cancelled') && (
                  <span style={{color:'#aaa'}}>No Action</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      </div>
      {/* Edit Modal */}
      <Modal
        title="Edit Appointment"
        open={editModal.open}
        onOk={handleEditSave}
        onCancel={()=>setEditModal({open:false,apt:null})}
        okText="Save"
      >
        <div style={{marginBottom:12}}>
          <label>Date: </label>
          <input type="date" value={form.date} onChange={e=>setForm(f=>({...f,date:e.target.value}))} style={{marginLeft:8}} />
        </div>
        <div style={{marginBottom:12}}>
          <label>Time: </label>
          <input type="time" value={form.time} onChange={e=>setForm(f=>({...f,time:e.target.value}))} style={{marginLeft:8}} />
        </div>
        <div style={{marginBottom:12}}>
          <label>Notes: </label>
          <input type="text" value={form.notes} onChange={e=>setForm(f=>({...f,notes:e.target.value}))} style={{marginLeft:8,width:'70%'}} />
        </div>
      </Modal>
      {/* Cancel Modal */}
      <Modal
        title="Cancel Appointment"
        open={!!cancelId}
        onOk={confirmCancel}
        onCancel={()=>setCancelId(null)}
        okText="Yes, Cancel"
        okButtonProps={{danger:true}}
      >
        Are you sure you want to cancel this appointment?
      </Modal>
    </div>
  );
};

export default UserAppointments; 