import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Table, Tag, Space, message } from 'antd';
import { 
  UserOutlined, 
  ScissorOutlined, 
  CalendarOutlined, 
  DollarOutlined,
  ClockCircleOutlined
} from '@ant-design/icons';
import { getBarbers, getServices, getAppointments } from '../../api';
import { getUsers } from '../../api/userApi';
import './Dashboard.css';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalBarbers: 0,
    totalServices: 0,
    totalAppointments: 0,
    totalRevenue: 0,
    pendingAppointments: 0,
    todayAppointments: 0
  });

  const [recentAppointments, setRecentAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const [barbersRes, servicesRes, appointmentsRes, usersRes] = await Promise.all([
          getBarbers(),
          getServices(),
          getAppointments(),
          getUsers()
        ]);

        // Check if responses are valid
        if (!barbersRes?.data?.data || !servicesRes?.data?.data || !appointmentsRes?.data?.data || !usersRes?.data?.data) {
          throw new Error('Invalid response from server');
        }

        const barbers = Array.isArray(barbersRes.data.data) ? barbersRes.data.data : [];
        const services = Array.isArray(servicesRes.data.data) ? servicesRes.data.data : [];
        const appointments = Array.isArray(appointmentsRes.data.data) ? appointmentsRes.data.data : [];
        const users = Array.isArray(usersRes.data.data) ? usersRes.data.data : [];

        // Calculate total revenue
        const totalRevenue = appointments.reduce((sum, apt) => {
          const service = services.find(s => s.id === apt.service_id);
          return sum + (service ? service.price : 0);
        }, 0);

        // Get today's date in YYYY-MM-DD format
        const today = new Date().toISOString().split('T')[0];
        
        // Filter appointments
        const todayAppts = appointments.filter(apt => 
          apt.date && apt.date.split('T')[0] === today
        );

        const pendingAppts = appointments.filter(apt => 
          apt.status === 'pending'
        );

        // Sort appointments by date, most recent first
        const sortedAppointments = [...appointments]
          .sort((a, b) => new Date(b.appointment_date) - new Date(a.appointment_date))
          .slice(0, 5)
          .map(apt => ({
            ...apt,
            date: apt.appointment_date,
            time: apt.appointment_date,
            service: services.find(s => s.id === apt.service_id) || null,
            userEmail: users.find(u => String(u.id) === String(apt.user_id))?.email || 'N/A',
          }));

        setStats({
          totalBarbers: barbers.length,
          totalServices: services.length,
          totalAppointments: appointments.length,
          totalRevenue,
          pendingAppointments: pendingAppts.length,
          todayAppointments: todayAppts.length
        });

        setRecentAppointments(sortedAppointments);
        setUsers(users);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        setError('Failed to load dashboard data. Please try again later.');
        message.error('Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const getStatusColor = (status) => {
    const colors = {
      pending: 'gold',
      confirmed: 'blue',
      completed: 'green',
      cancelled: 'red'
    };
    return colors[status] || 'default';
  };

  const recentAppointmentsColumns = [
    {
      title: 'Email',
      dataIndex: 'userEmail',
      key: 'userEmail',
      render: (email) => email || 'N/A',
    },
    {
      title: 'Date',
      dataIndex: 'date',
      key: 'date',
      render: (date) => date ? new Date(date).toLocaleDateString() : 'N/A',
    },
    {
      title: 'Time',
      dataIndex: 'time',
      key: 'time',
      render: (time) => time ? new Date(time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 'N/A',
    },
    {
      title: 'Service',
      dataIndex: 'service',
      key: 'service',
      render: (service) => service?.name || 'N/A',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={getStatusColor(status)}>
          {status ? status.toUpperCase() : 'N/A'}
        </Tag>
      ),
    },
  ];

  if (error) {
    return (
      <div className="admin-dashboard">
        <h1>Admin Dashboard</h1>
        <Card>
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <p style={{ color: 'red' }}>{error}</p>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="admin-dashboard">
      <h1>Admin Dashboard</h1>
      
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Card loading={loading}>
            <Statistic
              title="Total Barbers"
              value={stats.totalBarbers}
              prefix={<ScissorOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Card loading={loading}>
            <Statistic
              title="Total Services"
              value={stats.totalServices}
              prefix={<DollarOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Card loading={loading}>
            <Statistic
              title="Total Appointments"
              value={stats.totalAppointments}
              prefix={<CalendarOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Card loading={loading}>
            <Statistic
              title="Total Revenue"
              value={stats.totalRevenue}
              prefix={<DollarOutlined />}
              precision={2}
              formatter={(value) => `$${value.toLocaleString()}`}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Card loading={loading}>
            <Statistic
              title="Pending Appointments"
              value={stats.pendingAppointments}
              prefix={<ClockCircleOutlined />}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Card loading={loading}>
            <Statistic
              title="Today's Appointments"
              value={stats.todayAppointments}
              prefix={<CalendarOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
      </Row>

      <Card 
        title="Recent Appointments" 
        style={{ marginTop: 24 }}
        loading={loading}
      >
        <Table 
          columns={recentAppointmentsColumns} 
          dataSource={recentAppointments}
          rowKey="id"
          pagination={false}
        />
      </Card>
    </div>
  );
};

export default Dashboard; 