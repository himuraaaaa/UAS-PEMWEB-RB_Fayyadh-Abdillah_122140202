import React, { useState, useEffect } from 'react';
import { Table, Tag, Button, Select, Space, message } from 'antd';
import { getAppointments, updateAppointmentStatus, getBarbers, getServices } from '../../api';

const { Option } = Select;

const AppointmentManagement = () => {
  const [appointments, setAppointments] = useState([]);
  const [barbers, setBarbers] = useState([]);
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchAppointments = async () => {
    setLoading(true);
    try {
      const [appointmentsRes, barbersRes, servicesRes] = await Promise.all([
        getAppointments(),
        getBarbers(),
        getServices()
      ]);
      const appointmentsData = appointmentsRes?.data?.data || [];
      const barbersData = barbersRes?.data?.data || [];
      const servicesData = servicesRes?.data?.data || [];

      // Mapping barber & service name
      const mappedAppointments = appointmentsData.map(apt => ({
        ...apt,
        barber: barbersData.find(b => b.id === apt.barber_id) || null,
        service: servicesData.find(s => s.id === apt.service_id) || null,
      }));
      setAppointments(mappedAppointments);
      setBarbers(barbersData);
      setServices(servicesData);
    } catch (error) {
      message.error('Failed to fetch appointments/barbers/services');
      setAppointments([]);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchAppointments();
  }, []);

  const handleStatusChange = async (id, newStatus) => {
    try {
      await updateAppointmentStatus(id, { status: newStatus });
      message.success('Appointment status updated successfully');
      fetchAppointments();
    } catch (error) {
      message.error(error.response?.data?.message || 'Failed to update appointment status');
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      pending: 'gold',
      confirmed: 'blue',
      completed: 'green',
      cancelled: 'red'
    };
    return colors[status] || 'default';
  };

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
    },
    {
      title: 'Date',
      dataIndex: 'date',
      key: 'date',
      render: (date) => new Date(date).toLocaleDateString(),
    },
    {
      title: 'Time',
      dataIndex: 'time',
      key: 'time',
    },
    {
      title: 'Barber',
      dataIndex: 'barber',
      key: 'barber',
      render: (barber) => barber?.name || 'N/A',
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
          {status.toUpperCase()}
        </Tag>
      ),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space>
          <Select
            defaultValue={record.status}
            style={{ width: 120 }}
            onChange={(value) => handleStatusChange(record.id, value)}
          >
            <Option value="pending">Pending</Option>
            <Option value="confirmed">Confirmed</Option>
            <Option value="completed">Completed</Option>
            <Option value="cancelled">Cancelled</Option>
          </Select>
        </Space>
      ),
    },
  ];

  return (
    <div className="appointment-management">
      <h2>Appointment Management</h2>
      <Table
        columns={columns}
        dataSource={appointments}
        rowKey="id"
        loading={loading}
      />
    </div>
  );
};

export default AppointmentManagement; 