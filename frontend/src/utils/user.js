// 读取当前登录用户 ID（不存在返回 null）
export function currentUserId() {
  try {
    return JSON.parse(localStorage.getItem('user')).id;
  } catch {
    return null;
  }
}